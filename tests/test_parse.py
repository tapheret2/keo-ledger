from pathlib import Path

from keo_ledger.parse import parse_filename
from keo_ledger.settle import settle_ticket, winrate


def test_parse():
    t = parse_filename(Path("2026-07-08_jonny_denmark-italy_U2.5_FT.jpg"))
    assert t and t.tipster == "jonny" and t.market == "U2.5"


def test_settle_u25():
    assert settle_ticket("U2.5", "0-0") == "W"
    assert settle_ticket("O1.5", "2-1") == "W"


def test_wr():
    assert winrate(["W", "L", "HALF_W"])["winrate"] == 0.5
