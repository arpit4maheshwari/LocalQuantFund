def format_weekly_report(summary: dict, signals: dict) -> str:
    lines = []
    lines.append(f"Weekly Market Summary (Week ending {summary['week_end']})\n")

    lines.append("Top performers:")
    for item in summary["top_symbols"]:
        sym = item["symbol"]
        ret = item["weekly_return"]
        lines.append(f"  - {sym}: {ret:.2%}")

    lines.append("\nBottom performers:")
    for item in summary["bottom_symbols"]:
        sym = item["symbol"]
        ret = item["weekly_return"]
        lines.append(f"  - {sym}: {ret:.2%}")

    # placeholder for future buy/sell suggestions
    if signals.get("buys"):
        lines.append("\nPotential buys:")
        for s in signals["buys"]:
            lines.append(f"  - {s}")

    if signals.get("sells"):
        lines.append("\nPotential sells:")
        for s in signals["sells"]:
            lines.append(f"  - {s}")

    return "\n".join(lines)
