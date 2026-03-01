from dotenv import load_dotenv

from analytics.weekly_summary import (
    load_prices,
    compute_weekly_returns,
    summarize_latest_week,
)
from analytics.llm_report import format_weekly_report
from app.telegram_client import TelegramClient

load_dotenv()


def main():
    prices = load_prices()
    weekly = compute_weekly_returns(prices)
    summary = summarize_latest_week(weekly)
    signals = {"buys": [], "sells": []}
    report_text = format_weekly_report(summary, signals)

    client = TelegramClient()
    client.send_message(report_text)

if __name__ == "__main__":
    main()
