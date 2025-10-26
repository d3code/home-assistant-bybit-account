"""Data update coordinator for Bybit Account integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from pybit.unified_trading import HTTP
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, ACCOUNT_CATEGORY

_LOGGER = logging.getLogger(__name__)


class BybitAccountDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching data from the Bybit API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize."""
        self.entry = entry
        self.api_key = entry.data["api_key"]
        self.api_secret = entry.data["api_secret"]
        self.scan_interval = entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)
        
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
        self.update_interval = timedelta(seconds=new_interval)
        _LOGGER.debug("Updated scan interval to %d seconds", new_interval)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via library."""
        try:
            _LOGGER.debug("Fetching Bybit account data")
            
            # Fetch position data
            _LOGGER.debug("Calling get_positions with category=%s, settleCoin=USDT", ACCOUNT_CATEGORY)
            positions_response = await self.hass.async_add_executor_job(
                lambda: self.session.get_positions(category=ACCOUNT_CATEGORY, settleCoin="USDT")
            )
            _LOGGER.debug("Positions response: %s", positions_response)
            
            # Fetch account balance
            _LOGGER.debug("Calling get_wallet_balance with accountType=UNIFIED")
            balance_response = await self.hass.async_add_executor_job(
                lambda: self.session.get_wallet_balance(accountType="UNIFIED")
            )
            _LOGGER.debug("Balance response: %s", balance_response)
            
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
