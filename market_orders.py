#!/usr/bin/env python3
"""
market_orders.py
CLI for placing market orders on Binance USDT-M Futures (dry-run by default).
Usage:
  python src/market_orders.py BTCUSDT BUY 0.001 --api-key YOUR_KEY --api-secret YOUR_SECRET
  python src/market_orders.py BTCUSDT SELL 0.01 --dry-run
"""

import argparse, time, os, json
from utils import BinanceFuturesClient, setup_logger, validate_symbol, validate_quantity

LOG = setup_logger()

def parse_args():
    p = argparse.ArgumentParser(description="Place a market order on Binance Futures (USDT-M).")
    p.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    p.add_argument("side", choices=["BUY","SELL"], help="BUY or SELL")
    p.add_argument("quantity", type=float, help="Quantity (contracts or base asset depending on pair)")
    p.add_argument("--api-key", type=str, default=os.getenv("BINANCE_API_KEY"), help="Binance API Key")
    p.add_argument("--api-secret", type=str, default=os.getenv("BINANCE_SECRET"), help="Binance API Secret")
    p.add_argument("--dry-run", action="store_true", help="If set, will not send real orders (default True)")
    return p.parse_args()

def main():
    args = parse_args()
    try:
        validate_symbol(args.symbol)
        validate_quantity(args.quantity)
    except ValueError as e:
        LOG.error("Validation error", extra={"error": str(e)})
        raise SystemExit(1)

    client = BinanceFuturesClient(api_key=args.api_key, api_secret=args.api_secret, dry_run=args.dry_run or (args.api_key is None))
    LOG.info("Placing market order", extra={"symbol": args.symbol, "side": args.side, "quantity": args.quantity})

    try:
        resp = client.place_market_order(symbol=args.symbol, side=args.side, quantity=args.quantity)
        LOG.info("Order response", extra={"response": resp})
        print(json.dumps(resp, indent=2))
    except Exception as e:
        LOG.exception("Failed to place market order")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
