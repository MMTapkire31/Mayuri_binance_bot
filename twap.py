"""
twap.py
Time-Weighted Average Price (TWAP) strategy example.
Split a large order into N equal slices and execute each slice at equal time intervals.
This implementation is simple and intended for educational use and backtesting/dry-run only.
"""

import time, logging, math
from utils import BinanceFuturesClient, setup_logger, validate_quantity

LOG = setup_logger()

def execute_twap(client, symbol, side, total_quantity, slices=5, interval_seconds=60):
    validate_quantity(total_quantity)
    slice_qty = total_quantity / slices
    executed = []
    for i in range(slices):
        LOG.info("TWAP slice %d/%d", i+1, slices, extra={"slice_qty": slice_qty})
        resp = client.place_market_order(symbol=symbol, side=side, quantity=round(slice_qty, 8))
        executed.append(resp)
        time.sleep(interval_seconds)
    return executed

if __name__ == "__main__":
    # Example dry-run usage
    c = BinanceFuturesClient(dry_run=True)
    print(execute_twap(c, "BTCUSDT", "BUY", 0.01, slices=4, interval_seconds=1))
