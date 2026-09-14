from models.discount import PercentageDiscount, FixedDiscount

def test_percentage_discount():
    assert PercentageDiscount(10).calculate(500, 2) == 100

def test_fixed_discount_cannot_exceed_total():
    assert FixedDiscount(1000).calculate(500, 1) == 500