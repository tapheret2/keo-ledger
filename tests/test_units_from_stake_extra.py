
from keo_ledger.ledger import settle_pnl, units_from_stake

def test_units_and_pnl():
    assert units_from_stake(50, 10) == 5
    assert settle_pnl(10, 2.0, True) == 10
    assert settle_pnl(10, 2.0, False) == -10
