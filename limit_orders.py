#!/usr/bin/env python3
"""
limit_orders.py
CLI for placing limit orders on Binance USDT-M Futures (dry-run by default).
Usage:
  python src/limit_orders.py BTCUSDT BUY 0.001 42000 --time-in-force GTC --dry-run
"""

import argparse, os, json
from utils import BinanceFuturesClient, setup_logger, validate_symbol, validate_quantity, validate_price

LOG = setup_logger()

def parse_args():
    p = argparse.ArgumentParser(description="Place a limit order on Binance Futures.")
    p.add_argument("symbol", type=str, help="Trading pair (e.g., BTCUSDT)")
    p.add_argument("side", choices=["BUY","SELL"], help="BUY or SELL")
    p.add_argument("quantity", type=float, help="Quantity")
    p.add_argument("price", type=float, help="Limit price")
    p.add_argument("--time-in-force", choices=["GTC","IOC","FOK"], default="GTC")
    p.add_argument("--api-key", type=str, default=os.getenv("BINANCE_API_KEY"))
    p.add_argument("--api-secret", type=str, default=os.getenv("BINANCE_SECRET"))
    p.add_argument("--dry-run", action="store_true", help="Do not send real orders")
    return p.parse_args()

def main():
    args = parse_args()
    try:
        validate_symbol(args.symbol)
        validate_quantity(args.quantity)
        validate_price(args.price)
    except ValueError as e:
        LOG.error("Validation error", extra={"error": str(e)})
        raise SystemExit(1)

    client = BinanceFuturesClient(api_key=args.api_key, api_secret=args.api_secret, dry_run=args.dry_run or (args.api_key is None))
    LOG.info("Placing limit order", extra={"symbol": args.symbol, "side": args.side, "quantity": args.quantity, "price": args.price})

    try:
        resp = client.place_limit_order(symbol=args.symbol, side=args.side, quantity=args.quantity, price=args.price, time_in_force=args.time_in_force)
        LOG.info("Order response", extra={"response": resp})
        print(json.dumps(resp, indent=2))
    except Exception as e:
        LOG.exception("Failed to place limit order")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
