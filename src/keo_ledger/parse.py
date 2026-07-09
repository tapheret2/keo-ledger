from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

NAME_RE = re.compile(
    r"^(?P<day>\d{4}-\d{2}-\d{2})_(?P<tipster>[^_]+)_(?P<match>.+)_(?P<market>[^_]+)_(?P<period>FT|HT|LIVE)\.",
    re.I,
)


@dataclass
class Ticket:
    day: str
    tipster: str
    match: str
    market: str
    period: str
    source_file: str
    result: str = "PENDING"  # W L PUSH HALF_W HALF_L VOID
    score: str = ""


def parse_filename(path: Path) -> Ticket | None:
    m = NAME_RE.match(path.name)
    if not m:
        return None
    d = m.groupdict()
    return Ticket(
        day=d["day"],
        tipster=d["tipster"].lower(),
        match=d["match"],
        market=d["market"].upper(),
        period=d["period"].upper(),
        source_file=str(path),
    )


def scan_dir(folder: Path) -> list[Ticket]:
    tickets: list[Ticket] = []
    for p in sorted(folder.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        if p.suffix.lower() in {".txt", ".md", ".cmd", ".ps1"} and p.name.upper().startswith("README"):
            continue
        t = parse_filename(p)
        if t:
            tickets.append(t)
    return tickets


def tickets_to_csv_rows(tickets: list[Ticket]) -> list[dict]:
    return [asdict(t) for t in tickets]
