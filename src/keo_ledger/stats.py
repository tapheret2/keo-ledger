"""Stats helpers."""

def roi(profit: float, stake: float) -> float:
    if stake <= 0:
        return 0.0
    return profit / stake
