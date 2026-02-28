"""Call LLM and format text for reports."""
def format_weekly_report(summary, signals):
    # For v0, just build strings without LLM
    text = "Weekly Market Summary\n\n"
    text += f"Week: {summary['week']}\n"
    text += "Top sectors: ...\n"
    text += "Bottom sectors: ...\n"
    # etc.
    return text
