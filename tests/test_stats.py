from keo_ledger.stats import winrate, record_summary

def test_winrate():
    assert abs(winrate(3, 1) - 0.75) < 1e-9

def test_record_summary():
    s = record_summary(2, 2)
    assert s["n"] == 4
    assert abs(s["winrate"] - 0.5) < 1e-9
