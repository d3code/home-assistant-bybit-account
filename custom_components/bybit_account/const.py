"""Constants for the Bybit Account integration."""

DOMAIN = "bybit_account"

# Default polling interval in seconds
DEFAULT_SCAN_INTERVAL = 60

# Bybit API configuration
API_BASE_URL = "https://api.bybit.com"
API_TESTNET_URL = "https://api-testnet.bybit.com"

# Account category for linear trading
ACCOUNT_CATEGORY = "linear"

# Sensor types
SENSOR_TYPES = {
    "unrealised_pnl": {
        "name": "Unrealised PnL",
        "unit_of_measurement": "USDT",
        "icon": "mdi:currency-usd",
        "device_class": "monetary",
    },
    "position_size": {
        "name": "Position Size",
        "unit_of_measurement": "USDT",
        "icon": "mdi:chart-line",
    },
    "leverage": {
        "name": "Leverage",
        "unit_of_measurement": "x",
        "icon": "mdi:gauge",
    },
    "avg_price": {
        "name": "Average Price",
        "unit_of_measurement": "USDT",
        "icon": "mdi:currency-usd",
        "device_class": "monetary",
    },
    "mark_price": {
        "name": "Mark Price",
        "unit_of_measurement": "USDT",
        "icon": "mdi:currency-usd",
        "device_class": "monetary",
    },
    "liq_price": {
        "name": "Liquidation Price",
        "unit_of_measurement": "USDT",
        "icon": "mdi:alert-circle",
        "device_class": "monetary",
    },
    "position_value": {
        "name": "Position Value",
        "unit_of_measurement": "USDT",
        "icon": "mdi:chart-pie",
        "device_class": "monetary",
    },
}

# Account-level sensor types
ACCOUNT_SENSOR_TYPES = {
    "total_equity": {
        "name": "Total Equity",
        "unit_of_measurement": "USDT",
        "icon": "mdi:wallet",
        "device_class": "monetary",
    },
    "available_balance": {
        "name": "Available Balance",
        "unit_of_measurement": "USDT",
        "icon": "mdi:wallet-outline",
        "device_class": "monetary",
    },
    "total_unrealised_pnl": {
        "name": "Total Unrealised PnL",
        "unit_of_measurement": "USDT",
        "icon": "mdi:currency-usd",
        "device_class": "monetary",
    },
}
