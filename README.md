# Bybit Account Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/d3code/home-assistant-bybit-account.svg)](https://github.com/d3code/home-assistant-bybit-account/releases)

A Home Assistant custom integration that connects to the Bybit API to monitor your trading positions and account balance in real-time.

## Features

- **Real-time Position Monitoring**: Track unrealised PnL, position size, leverage, and more for each trading position
- **Account Balance Tracking**: Monitor total equity, available balance, and wallet balance
- **Automatic Sensor Creation**: Sensors are automatically created/removed as positions are opened/closed
- **Configurable Update Interval**: Set custom polling intervals (30 seconds to 1 hour)
- **Secure Credential Storage**: API credentials are stored securely in Home Assistant's config entry
- **HACS Compatible**: Easy installation and updates through HACS

## Installation

### Method 1: HACS (Recommended)

1. Install [HACS](https://hacs.xyz/) if you haven't already
2. Open HACS in Home Assistant
3. Go to "Integrations"
4. Click the three dots menu and select "Custom repositories"
5. Add this repository URL: `https://github.com/d3code/home-assistant-bybit-account`
6. Set category to "Integration"
7. Click "Add"
8. Find "Bybit Account" in the integrations list and install it
9. Restart Home Assistant

### Method 2: Manual Installation

1. Download the latest release from the [releases page](https://github.com/d3code/home-assistant-bybit-account/releases)
2. Extract the `bybit_account` folder to your `custom_components` directory
3. Restart Home Assistant

## Configuration

### Step 1: Get Bybit API Credentials

1. Log in to your [Bybit account](https://www.bybit.com/)
2. Go to Account & Security → API Management
3. Create a new API key with the following permissions:
   - **Read** permissions for account and positions
   - **IP whitelist** (recommended for security)
4. Copy your API Key and API Secret

### Step 2: Add Integration in Home Assistant

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Bybit Account"
4. Enter your API credentials:
   - **API Key**: Your Bybit API key
   - **API Secret**: Your Bybit API secret
   - **Update Interval**: How often to fetch data (default: 60 seconds)
5. Click **Submit**

The integration will validate your credentials and create the necessary sensors.

## Available Sensors

### Account-Level Sensors

- **Bybit Total Equity**: Your total account equity in USDT
- **Bybit Available Balance**: Available balance for trading/withdrawal
- **Bybit Total Unrealised PnL**: Sum of unrealised PnL across all positions

### Position-Level Sensors (per trading pair)

For each active position, the following sensors are created:

- **Bybit [SYMBOL] Unrealised PnL**: Current unrealised profit/loss
- **Bybit [SYMBOL] Position Size**: Size of the position
- **Bybit [SYMBOL] Leverage**: Current leverage multiplier
- **Bybit [SYbit [SYMBOL] Average Price**: Average entry price
- **Bybit [SYMBOL] Mark Price**: Current mark price
- **Bybit [SYMBOL] Liquidation Price**: Price at which position would be liquidated
- **Bybit [SYMBOL] Position Value**: Total value of the position

### Sensor Attributes

Each sensor includes additional attributes such as:
- Position side (Buy/Sell)
- Position status (Normal/Liq/Adl)
- Take profit and stop loss levels
- Creation and update timestamps
- Current and cumulative realised PnL

## Configuration Options

You can modify the integration settings after installation:

1. Go to **Settings** → **Devices & Services**
2. Find "Bybit Account" and click **Configure**
3. Adjust the **Update Interval** (30-3600 seconds)

## Troubleshooting

### Common Issues

**"Invalid API credentials" error:**
- Verify your API key and secret are correct
- Ensure your API key has the required permissions
- Check if your IP is whitelisted (if IP whitelist is enabled)

**"Unable to connect to Bybit API" error:**
- Check your internet connection
- Verify Bybit API is not experiencing outages
- Check Home Assistant logs for detailed error messages

**Sensors not updating:**
- Verify the update interval is not too long
- Check Home Assistant logs for API errors
- Ensure your Bybit account has active positions (for position sensors)

### Logs

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.bybit_account: debug
```

### Support

- **Issues**: [GitHub Issues](https://github.com/d3code/home-assistant-bybit-account/issues)
- **Discussions**: [GitHub Discussions](https://github.com/d3code/home-assistant-bybit-account/discussions)

## API Information

This integration uses the [Bybit V5 API](https://bybit-exchange.github.io/docs/v5/position) and supports:
- **Account Type**: Unified Trading Account (UTA)
- **Category**: Linear (USDT Perpetual contracts)
- **Environment**: Mainnet only

## Security

- API credentials are stored securely in Home Assistant's encrypted config
- No credentials are logged or transmitted outside of Home Assistant
- Consider using IP whitelisting on your Bybit API key for additional security

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not affiliated with Bybit. Use at your own risk. Trading cryptocurrencies involves substantial risk and may not be suitable for all investors.
