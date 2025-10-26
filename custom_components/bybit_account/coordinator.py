"""Data update coordinator for Bybit Account integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from pybit.unified_trading import HTTP
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, ACCOUNT_CATEGORY, MIN_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class BybitAccountDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching data from the Bybit API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self.api_key = entry.data["api_key"]
        self.api_secret = entry.data["api_secret"]
        self.scan_interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        
        # Rate limiting safety features
        self._backoff_delay = 0
        self._consecutive_failures = 0
        self._rate_limit_warnings = 0
        self._original_interval = self.scan_interval
        
        # Initialize Bybit session
        self.session = HTTP(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=False,  # Only support mainnet
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=self.scan_interval),
        )

    def update_scan_interval(self, new_interval: int) -> None:
        """Update the scan interval."""
        self.scan_interval = new_interval
        self._original_interval = new_interval
        self.update_interval = timedelta(seconds=new_interval)
        _LOGGER.debug("Updated scan interval to %d seconds", new_interval)

    def _handle_rate_limit_response(self, response: dict[str, Any], headers: dict[str, str]) -> None:
        """Handle rate limit monitoring and warnings."""
        # Check for rate limit headers
        if 'X-Bapi-Limit-Status' in headers:
            remaining = int(headers['X-Bapi-Limit-Status'])
            limit = int(headers.get('X-Bapi-Limit', '0'))
            
            if remaining < 10:  # Safety threshold
                self._rate_limit_warnings += 1
                _LOGGER.warning(
                    "Rate limit approaching: %d/%d requests remaining (warning #%d)",
                    remaining, limit, self._rate_limit_warnings
                )
                
                # Temporarily increase interval if we're getting close
                if remaining < 5 and self.scan_interval < self._original_interval * 2:
                    new_interval = min(self._original_interval * 2, 300)  # Max 5 minutes
                    self.update_interval = timedelta(seconds=new_interval)
                    _LOGGER.warning("Temporarily increased interval to %d seconds due to rate limit", new_interval)
            else:
                # Reset warnings if we're back to safe levels
                if self._rate_limit_warnings > 0:
                    _LOGGER.info("Rate limit back to safe levels: %d/%d requests remaining", remaining, limit)
                    self._rate_limit_warnings = 0
                    
                    # Restore original interval if it was temporarily increased
                    if self.scan_interval != self._original_interval:
                        self.update_interval = timedelta(seconds=self._original_interval)
                        _LOGGER.info("Restored original interval to %d seconds", self._original_interval)

    def _handle_rate_limit_error(self, response: dict[str, Any]) -> bool:
        """Handle rate limit errors and implement backoff."""
        ret_code = response.get("retCode")
        ret_msg = response.get("retMsg", "")
        
        if ret_code == 10006 or "Too many visits" in ret_msg:
            self._consecutive_failures += 1
            self._backoff_delay = min(2 ** self._consecutive_failures, 60)  # Max 60 seconds
            
            _LOGGER.error(
                "Rate limit exceeded (error #%d): %s. Backing off for %d seconds",
                self._consecutive_failures, ret_msg, self._backoff_delay
            )
            
            # Temporarily increase interval significantly
            emergency_interval = max(self._original_interval * 4, 300)  # At least 5 minutes
            self.update_interval = timedelta(seconds=emergency_interval)
            _LOGGER.warning("Emergency interval set to %d seconds due to rate limit", emergency_interval)
            
            return True
        
        return False

    def _reset_backoff_on_success(self) -> None:
        """Reset backoff and failure counters on successful request."""
        if self._consecutive_failures > 0:
            _LOGGER.info("API requests successful, resetting failure counters")
            self._consecutive_failures = 0
            self._backoff_delay = 0
            
            # Restore original interval if it was changed due to failures
            if self.scan_interval != self._original_interval:
                self.update_interval = timedelta(seconds=self._original_interval)
                _LOGGER.info("Restored original interval to %d seconds", self._original_interval)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        # Apply backoff delay if we had previous failures
        if self._backoff_delay > 0:
            _LOGGER.debug("Applying backoff delay of %d seconds", self._backoff_delay)
            await asyncio.sleep(self._backoff_delay)
        
        try:
            _LOGGER.debug("Fetching Bybit account data")
            
            # Fetch position data
            _LOGGER.debug("Calling get_positions with category=%s, settleCoin=USDT", ACCOUNT_CATEGORY)
            positions_response = await self.hass.async_add_executor_job(
                lambda: self.session.get_positions(category=ACCOUNT_CATEGORY, settleCoin="USDT")
            )
            _LOGGER.debug("Positions response: %s", positions_response)
            
            # Check for rate limit errors in positions response
            if self._handle_rate_limit_error(positions_response):
                raise UpdateFailed("Rate limit exceeded for positions request")
            
            # Fetch account balance
            _LOGGER.debug("Calling get_wallet_balance with accountType=UNIFIED")
            balance_response = await self.hass.async_add_executor_job(
                lambda: self.session.get_wallet_balance(accountType="UNIFIED")
            )
            _LOGGER.debug("Balance response: %s", balance_response)
            
            # Check for rate limit errors in balance response
            if self._handle_rate_limit_error(balance_response):
                raise UpdateFailed("Rate limit exceeded for balance request")
            
            # Reset backoff on successful requests
            self._reset_backoff_on_success()
            
            # Process positions data
            positions = []
            if positions_response.get("retCode") == 0:
                positions = positions_response.get("result", {}).get("list", [])
                _LOGGER.debug("Fetched %d positions", len(positions))
            else:
                _LOGGER.warning(
                    "Failed to fetch positions: %s", 
                    positions_response.get("retMsg", "Unknown error")
                )
            
            # Process balance data
            balance_data = {}
            if balance_response.get("retCode") == 0:
                balance_list = balance_response.get("result", {}).get("list", [])
                if balance_list:
                    # Get USDT balance (primary trading currency)
                    usdt_balance = next(
                        (item for item in balance_list if item.get("coin") == "USDT"),
                        {}
                    )
                    balance_data = {
                        "total_equity": usdt_balance.get("totalEquity", "0"),
                        "available_balance": usdt_balance.get("availableToWithdraw", "0"),
                        "wallet_balance": usdt_balance.get("walletBalance", "0"),
                    }
                _LOGGER.debug("Fetched balance data: %s", balance_data)
            else:
                _LOGGER.warning(
                    "Failed to fetch balance: %s", 
                    balance_response.get("retMsg", "Unknown error")
                )
            
            # Calculate total unrealised PnL across all positions
            total_unrealised_pnl = 0.0
            for position in positions:
                try:
                    unrealised_pnl = float(position.get("unrealisedPnl", "0"))
                    total_unrealised_pnl += unrealised_pnl
                except (ValueError, TypeError):
                    continue
            
            return {
                "positions": positions,
                "balance": balance_data,
                "total_unrealised_pnl": total_unrealised_pnl,
                "last_update": self.hass.config.time_zone,
            }
            
        except Exception as err:
            _LOGGER.error("Error communicating with Bybit API: %s", err)
            _LOGGER.error("Error type: %s", type(err).__name__)
            _LOGGER.error("Error details: %s", str(err))
            raise UpdateFailed(f"Error communicating with Bybit API: {err}") from err
