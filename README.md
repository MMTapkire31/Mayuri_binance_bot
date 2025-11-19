# Mayuri - Binance Futures Order Bot

## Overview
This project is a CLI-based trading bot scaffold for **Binance USDT-M Futures**. It supports Market and Limit orders (core) and contains conceptual implementations for advanced orders (OCO, TWAP). The code defaults to **dry-run** if API keys are not provided to prevent accidental live trades.

**Important:** Always test with testnet keys and small sizes before using real funds.

## Structure
/src
market_orders.py
limit_orders.py
utils.py
/advanced
oco.py
twap.py
bot.log
report.pdf
README.md

## Requirements
- Python 3.8+
- `requests`

Install dependencies:
pip install -r requirements.txt


## Usage examples
Dry-run market order (safe):

python src/market_orders.py BTCUSDT BUY 0.001 --dry-run


Dry-run limit order:


python src/limit_orders.py BTCUSDT SELL 0.001 42000 --dry-run


Using real API keys (BE CAREFUL):


export BINANCE_API_KEY=your_api_key
export BINANCE_SECRET=your_api_secret
python src/market_orders.py BTCUSDT BUY 0.001


## Advanced orders (conceptual)
- `src/advanced/oco.py`: Shows how to place a take-profit limit and a stop-limit order and explains the monitoring needed.
- `src/advanced/twap.py`: Example TWAP implementation that slices an order over time (dry-run friendly).

## Logging
All actions and errors are logged to `bot.log` in a structured JSON-like format. By default the logger also prints INFO to stdout.

## Reproducibility & Notes
- Do **not** hardcode API keys in source files.
- For actual trading, use Binance Futures Testnet and proper order monitoring (websockets) before using live funds.
- The scaffold contains minimal validation; extend it with symbol info from exchange (e.g., step size, tick size).
