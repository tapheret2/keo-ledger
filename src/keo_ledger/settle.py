from __future__ import annotations

import re
from typing import Any


def parse_market(market: str) -> tuple[str, float] | None:
    m = re.match(r"^(O|U|AH)([+-]?\d+(?:\.\d+)?)$", market.upper())
    if not m:
        return None
    return m.group(1), float(m.group(2))


def settle_ou(side: str, line: float, total_goals: float) -> str:
    """side O or U."""
    # half lines
    if abs(line * 4 - round(line * 4)) < 1e-9 and (line * 4) % 1 == 0.0:
        pass
    # quarter lines
    frac = abs(line) - int(abs(line))
    if abs(frac - 0.25) < 1e-9 or abs(frac - 0.75) < 1e-9:
        # simplified: treat as nearest .0/.5 with half results
        base = int(line) + (0.5 if frac >= 0.5 else 0.0)
        if side == "O":
            if total_goals > line:
                return "W"
            if total_goals < base:
                return "L"
            return "HALF_W" if total_goals > base else "HALF_L"
        else:
            if total_goals < line:
                return "W"
            if total_goals > base + 0.5:
                return "L"
            return "HALF_W" if total_goals < base + 0.5 else "HALF_L"

    if abs(line - round(line)) < 1e-9:  # integer line → push possible
        if total_goals == line:
            return "PUSH"
        if side == "O":
            return "W" if total_goals > line else "L"
        return "W" if total_goals < line else "L"

    # .5 lines
    if side == "O":
        return "W" if total_goals > line else "L"
    return "W" if total_goals < line else "L"


def settle_ticket(market: str, score: str) -> str:
    """score like '2-1' full-time total goals."""
    parsed = parse_market(market)
    if not parsed:
        return "VOID"
    side, line = parsed
    if side == "AH":
        return "VOID"  # needs home/away goals + side — leave manual
    m = re.match(r"^(\d+)\s*[-:]\s*(\d+)$", score.strip())
    if not m:
        return "PENDING"
    total = int(m.group(1)) + int(m.group(2))
    return settle_ou(side, line, float(total))


def winrate(results: list[str]) -> dict[str, Any]:
    points = 0.0
    n = 0
    for r in results:
        if r in {"PENDING", "VOID", "PUSH"}:
            continue
        n += 1
        if r == "W":
            points += 1
        elif r.startswith("HALF_W"):
            points += 0.5
        elif r.startswith("HALF_L"):
            points += 0.0
        # L = 0
    return {"n": n, "points": points, "winrate": (points / n) if n else None}
