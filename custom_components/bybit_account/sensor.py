"""Sensor platform for Bybit Account integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    ACCOUNT_SENSOR_TYPES,
)
from .coordinator import BybitAccountDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bybit Account sensor based on a config entry."""
    coordinator: BybitAccountDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []

    # Add account-level sensors
    for sensor_type, sensor_info in ACCOUNT_SENSOR_TYPES.items():
        entities.append(
            BybitAccountSensor(
                coordinator=coordinator,
                sensor_type=sensor_type,
                sensor_info=sensor_info,
            )
        )

    # Add position-specific sensors
    if coordinator.data and "positions" in coordinator.data:
        for position in coordinator.data["positions"]:
            symbol = position.get("symbol", "")
            if symbol:  # Only create sensors for positions with valid symbols
                for sensor_type, sensor_info in SENSOR_TYPES.items():
                    entities.append(
                        BybitPositionSensor(
                            coordinator=coordinator,
                            position=position,
                            sensor_type=sensor_type,
                            sensor_info=sensor_info,
                        )
                    )

    async_add_entities(entities)


class BybitAccountSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Bybit Account sensor."""

    def __init__(
        self,
        coordinator: BybitAccountDataUpdateCoordinator,
        sensor_type: str,
        sensor_info: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._attr_name = f"Bybit {sensor_info['name']}"
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{sensor_type}"
        self._attr_icon = sensor_info.get("icon")
        self._attr_native_unit_of_measurement = sensor_info.get("unit_of_measurement")
        self._attr_device_class = sensor_info.get("device_class")

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        if self._sensor_type == "total_unrealised_pnl":
            return str(self.coordinator.data.get("total_unrealised_pnl", 0))
        
        balance_data = self.coordinator.data.get("balance", {})
        return balance_data.get(self._sensor_type, "0")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        return {
            "last_update": self.coordinator.data.get("last_update"),
            "scan_interval": self.coordinator.scan_interval,
        }


class BybitPositionSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Bybit Position sensor."""

    def __init__(
        self,
        coordinator: BybitAccountDataUpdateCoordinator,
        position: dict[str, Any],
        sensor_type: str,
        sensor_info: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._position = position
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._symbol = position.get("symbol", "")
        
        self._attr_name = f"Bybit {self._symbol} {sensor_info['name']}"
        self._attr_unique_id = f"{coordinator.entry.entry_id}_{self._symbol}_{sensor_type}"
        self._attr_icon = sensor_info.get("icon")
        self._attr_native_unit_of_measurement = sensor_info.get("unit_of_measurement")
        self._attr_device_class = sensor_info.get("device_class")

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        # Find the current position data
        current_position = None
        for position in self.coordinator.data.get("positions", []):
            if position.get("symbol") == self._symbol:
                current_position = position
                break

        if not current_position:
            return None

        # Map sensor types to position data fields
        field_mapping = {
            "unrealised_pnl": "unrealisedPnl",
            "position_size": "size",
            "leverage": "leverage",
            "avg_price": "avgPrice",
            "mark_price": "markPrice",
            "liq_price": "liqPrice",
            "position_value": "positionValue",
        }

        field_name = field_mapping.get(self._sensor_type)
        if field_name:
            value = current_position.get(field_name, "0")
            # Handle empty liquidation price
            if self._sensor_type == "liq_price" and value == "":
                return "0"
            return value

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}

        # Find the current position data
        current_position = None
        for position in self.coordinator.data.get("positions", []):
            if position.get("symbol") == self._symbol:
                current_position = position
                break

        if not current_position:
            return {}

        return {
            "symbol": current_position.get("symbol"),
            "side": current_position.get("side"),
            "position_status": current_position.get("positionStatus"),
            "trade_mode": current_position.get("tradeMode"),
            "auto_add_margin": current_position.get("autoAddMargin"),
            "take_profit": current_position.get("takeProfit"),
            "stop_loss": current_position.get("stopLoss"),
            "trailing_stop": current_position.get("trailingStop"),
            "cur_realised_pnl": current_position.get("curRealisedPnl"),
            "cum_realised_pnl": current_position.get("cumRealisedPnl"),
            "created_time": current_position.get("createdTime"),
            "updated_time": current_position.get("updatedTime"),
            "last_update": self.coordinator.data.get("last_update"),
            "scan_interval": self.coordinator.scan_interval,
        }
