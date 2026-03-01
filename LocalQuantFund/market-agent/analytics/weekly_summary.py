import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/prices_daily.parquet")


def load_prices() -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)
    # Expect columns: date, close, volume, symbol
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["symbol", "date"])
    return df


def compute_weekly_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute simple weekly close-to-close returns per symbol.
    """
    df = df.set_index("date")

    weekly_list = []
    for sym, grp in df.groupby("symbol"):
        # Take last close of each week, then pct_change across weeks
        weekly_close = grp["close"].resample("W-FRI").last()
        weekly_ret = weekly_close.pct_change()
        tmp = pd.DataFrame({
            "date": weekly_ret.index,
            "symbol": sym,
            "weekly_return": weekly_ret.values,
        })
        weekly_list.append(tmp)

    weekly_df = pd.concat(weekly_list, ignore_index=True)
    weekly_df = weekly_df.dropna(subset=["weekly_return"])
    return weekly_df


def summarize_latest_week(weekly_df: pd.DataFrame) -> dict:
    """
    Get the latest week in the data and build a simple summary:
    - best and worst symbols by weekly return.
    """
    latest_date = weekly_df["date"].max()
    latest_week = weekly_df[weekly_df["date"] == latest_date].copy()
    latest_week = latest_week.sort_values("weekly_return", ascending=False)

    top = latest_week.head(3).to_dict(orient="records")
    bottom = latest_week.tail(3).to_dict(orient="records")

    summary = {
        "week_end": latest_date.date().isoformat(),
        "top_symbols": top,
        "bottom_symbols": bottom,
    }
    return summary


def run_weekly_summary_example():
    prices = load_prices()
    weekly = compute_weekly_returns(prices)
    summary = summarize_latest_week(weekly)
    print(summary)


if __name__ == "__main__":
    run_weekly_summary_example()
