"""Constants for the Bybit Account integration."""

DOMAIN = "bybit_account"

# Default polling interval in seconds
DEFAULT_SCAN_INTERVAL = 60

# Minimum and maximum polling intervals
MIN_SCAN_INTERVAL = 5
MAX_SCAN_INTERVAL = 3600

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
    # Account-level totals (USD values)
    "total_equity": {
        "name": "Total Equity",
        "unit_of_measurement": "USD",
        "icon": "mdi:wallet",
        "device_class": "monetary",
    },
    "total_wallet_balance": {
        "name": "Total Wallet Balance",
        "unit_of_measurement": "USD",
        "icon": "mdi:wallet",
        "device_class": "monetary",
    },
    "total_margin_balance": {
        "name": "Total Margin Balance",
        "unit_of_measurement": "USD",
        "icon": "mdi:chart-line",
        "device_class": "monetary",
    },
    "total_available_balance": {
        "name": "Total Available Balance",
        "unit_of_measurement": "USD",
        "icon": "mdi:wallet-outline",
        "device_class": "monetary",
    },
    "total_perp_upl": {
        "name": "Total Perp UPL",
        "unit_of_measurement": "USD",
        "icon": "mdi:chart-line",
        "device_class": "monetary",
    },
    "total_initial_margin": {
        "name": "Total Initial Margin",
        "unit_of_measurement": "USD",
        "icon": "mdi:shield",
        "device_class": "monetary",
    },
    "total_maintenance_margin": {
        "name": "Total Maintenance Margin",
        "unit_of_measurement": "USD",
        "icon": "mdi:shield-check",
        "device_class": "monetary",
    },
    
    # Account rates
    "account_im_rate": {
        "name": "Account IM Rate",
        "unit_of_measurement": "%",
        "icon": "mdi:percent",
        "device_class": None,
    },
    "account_mm_rate": {
        "name": "Account MM Rate",
        "unit_of_measurement": "%",
        "icon": "mdi:percent",
        "device_class": None,
    },
    
    # USDT-specific metrics
    "usdt_wallet_balance": {
        "name": "USDT Wallet Balance",
        "unit_of_measurement": "USDT",
        "icon": "mdi:currency-usd",
        "device_class": "monetary",
    },
    "usdt_available_to_withdraw": {
        "name": "USDT Available to Withdraw",
        "unit_of_measurement": "USDT",
        "icon": "mdi:wallet-outline",
        "device_class": "monetary",
    },
    "usdt_equity": {
        "name": "USDT Equity",
        "unit_of_measurement": "USDT",
        "icon": "mdi:wallet",
        "device_class": "monetary",
    },
    "usdt_unrealised_pnl": {
        "name": "USDT Unrealised PnL",
        "unit_of_measurement": "USDT",
        "icon": "mdi:chart-line",
        "device_class": "monetary",
    },
    "usdt_usd_value": {
        "name": "USDT USD Value",
        "unit_of_measurement": "USD",
        "icon": "mdi:currency-usd",
        "device_class": "monetary",
    },
    "usdt_borrow_amount": {
        "name": "USDT Borrow Amount",
        "unit_of_measurement": "USDT",
        "icon": "mdi:bank",
        "device_class": "monetary",
    },
    "usdt_accrued_interest": {
        "name": "USDT Accrued Interest",
        "unit_of_measurement": "USDT",
        "icon": "mdi:percent",
        "device_class": "monetary",
    },
    
    # Calculated total
    "total_unrealised_pnl": {
        "name": "Total Unrealised PnL",
        "unit_of_measurement": "USDT",
        "icon": "mdi:chart-line",
        "device_class": "monetary",
    },
}
