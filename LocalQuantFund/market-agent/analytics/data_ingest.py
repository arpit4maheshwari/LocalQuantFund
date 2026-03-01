import os
import time
from typing import List

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPHAVANTAGE_BASE_URL = "https://www.alphavantage.co/query"


def fetch_alpha_vantage_daily(symbol: str) -> pd.DataFrame:
    """
    Use Alpha Vantage FREE tier: TIME_SERIES_DAILY, compact output (last ~100 days).
    """
    if not ALPHAVANTAGE_API_KEY:
        raise ValueError("ALPHAVANTAGE_API_KEY not set in environment")

    params = {
        "function": "TIME_SERIES_DAILY",      # <- changed
        "symbol": symbol,
        "outputsize": "compact",              # free tier: up to 100 data points
        "apikey": ALPHAVANTAGE_API_KEY,
    }

    resp = requests.get(ALPHAVANTAGE_BASE_URL, params=params, timeout=30)
    data = resp.json()

    key = "Time Series (Daily)"
    if key not in data:
        # Handle common Alpha Vantage messages more nicely
        if "Information" in data or "Note" in data or "Error Message" in data:
            raise ValueError(f"Alpha Vantage error for {symbol}: {data}")
        raise ValueError(f"Unexpected response for {symbol}: {data}")

    ts = data[key]
    df = pd.DataFrame.from_dict(ts, orient="index")
    # TIME_SERIES_DAILY gives close, not adjusted close
    df = df[["4. close", "5. volume"]].rename(
        columns={"4. close": "close", "5. volume": "volume"}
    )
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df.astype(float)
    df["symbol"] = symbol
    return df



def fetch_equity_data(symbols: List[str]) -> pd.DataFrame:
    """
    Fetch daily data for a small list of symbols using FREE tier limits:
    - Max 5 requests per minute -> sleep ~15 seconds between requests.
    - Max 25 requests per day -> keep symbol list small or stagger days.
    """
    all_dfs = []
    for i, sym in enumerate(symbols):
        print(f"Fetching equity data for {sym} ({i+1}/{len(symbols)})")
        df = fetch_alpha_vantage_daily(sym)
        all_dfs.append(df)

        if i < len(symbols) - 1:
            # simple rate limiting: 5 calls/minute => ~12 seconds; use 15 for safety
            time.sleep(15)

    merged = pd.concat(all_dfs)
    merged.reset_index(inplace=True)
    merged.rename(columns={"index": "date"}, inplace=True)
    return merged


def save_to_parquet(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


def run_ingest_example():
    # Keep this small to stay within free daily quota
    symbols = ["AAPL", "MSFT", "NVDA"]  # adjust as needed
    prices_df = fetch_equity_data(symbols)
    save_to_parquet(prices_df, "data/prices_daily.parquet")


if __name__ == "__main__":
    run_ingest_example()
