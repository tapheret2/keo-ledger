from keo_ledger.stats import roi

def test_roi():
    assert abs(roi(25, 100) - 0.25) < 1e-9
    assert roi(10, 0) == 0.0
