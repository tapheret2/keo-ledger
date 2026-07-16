"""Stats helpers."""

def roi(profit: float, stake: float) -> float:
    if stake <= 0:
        return 0.0
    return profit / stake


def simple_roi(profit: float, staked: float) -> float:
    """ROI = profit / staked (0 if no stake)."""
    if staked <= 0:
        return 0.0
    return profit / staked
