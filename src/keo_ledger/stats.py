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


def hit_rate(wins: int, losses: int) -> float:
    """Win rate wins/(wins+losses); 0 if no settled tips."""
    total = int(wins) + int(losses)
    if total <= 0:
        return 0.0
    return int(wins) / total


def max_losing_streak(results: list[bool]) -> int:
    """Longest consecutive False (loss) run."""
    best = cur = 0
    for r in results:
        if r:
            cur = 0
        else:
            cur += 1
            best = max(best, cur)
    return best
