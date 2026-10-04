"""Download the full BTCUSDT 1-hour history from Binance for the same period
as the ETH and XRP files (2019-12-31 23:00 to 2025-10-08 09:00 UTC)."""

import os
import time
import requests
import pandas as pd

URL = "https://api.binance.com/api/v3/klines"
START = int(pd.Timestamp("2019-12-31 23:00", tz="UTC").timestamp() * 1000)
END = int(pd.Timestamp("2025-10-08 09:00", tz="UTC").timestamp() * 1000)
HOUR = 3_600_000
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume", "close_time",
           "quote_asset_volume", "number_of_trades", "taker_buy_base_volume",
           "taker_buy_quote_volume", "ignore"]

rows, start = [], START
while start <= END:
    params = {"symbol": "BTCUSDT", "interval": "1h", "startTime": start, "endTime": END, "limit": 1000}
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    batch = response.json()
    if not batch:
        break
    rows.extend(batch)
    start = batch[-1][0] + HOUR
    print(f"Downloaded up to {pd.to_datetime(batch[-1][0], unit='ms')}  ({len(rows):,} rows)")
    time.sleep(0.2)

df = pd.DataFrame(rows, columns=COLUMNS)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df = df.drop_duplicates("timestamp")

os.makedirs("binance_data", exist_ok=True)
path = os.path.join("binance_data", "BTCUSDT_1h_2025-10-08.csv")
df.to_csv(path, index=False)
print(f"Saved {len(df):,} rows to {path}")
