def format_amount(amount: int) -> str:
    if amount >= 1_000_000_000:
        v = amount / 1_000_000_000
        return f"{v:g}B"
    if amount >= 1_000_000:
        v = amount / 1_000_000
        return f"{v:g}M"
    if amount >= 1_000:
        v = amount / 1_000
        return f"{v:g}K"
    return str(amount)
