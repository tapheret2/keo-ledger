from keo_ledger.settle import profit_units, roi

def test_profit_win():
    assert abs(profit_units(10, 2.0, True) - 10) < 1e-12

def test_profit_loss():
    assert abs(profit_units(10, 2.0, False) + 10) < 1e-12

def test_roi():
    assert abs(roi(5, 10) - 0.5) < 1e-12
