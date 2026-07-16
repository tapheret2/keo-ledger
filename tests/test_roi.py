from keo_ledger.stats import simple_roi

def test_simple_roi():
    assert abs(simple_roi(20, 100) - 0.2) < 1e-9
    assert simple_roi(10, 0) == 0.0
