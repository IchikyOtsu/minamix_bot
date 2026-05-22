import math


def format_amount(amount: int) -> str:
    def _fmt(value: float) -> str:
        floored = math.floor(value * 10) / 10
        return f"{floored:.1f}".rstrip("0").rstrip(".")

    if amount >= 1_000_000_000:
        return f"{_fmt(amount / 1_000_000_000)}B"
    if amount >= 1_000_000:
        return f"{_fmt(amount / 1_000_000)}M"
    if amount >= 1_000:
        return f"{_fmt(amount / 1_000)}K"
    return str(amount)
