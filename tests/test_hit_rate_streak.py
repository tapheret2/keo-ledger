from keo_ledger.stats import hit_rate, max_losing_streak

def test_hit_rate():
    assert abs(hit_rate(3, 1) - 0.75) < 1e-12
    assert hit_rate(0, 0) == 0.0

def test_max_losing_streak():
    assert max_losing_streak([True, False, False, True, False]) == 2
