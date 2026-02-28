"""Script to run weekly market report generation."""
from analytics.weekly_summary import compute_weekly_sector_summary, generate_stock_signals
from analytics.llm_report import format_weekly_report
from app.whatsapp_client import send_message  # you'll implement

TO_NUMBER = "<your_personal_whatsapp_number>"

def main():
    summary = compute_weekly_sector_summary()
    signals = generate_stock_signals()
    report_text = format_weekly_report(summary, signals)
    send_message(TO_NUMBER, report_text)

if __name__ == "__main__":
    main()
