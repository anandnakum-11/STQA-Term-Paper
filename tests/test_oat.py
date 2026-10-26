import pytest
from src.discount_system import calculate_discount

# L4-style representative combinations used in the paper.
@pytest.mark.parametrize("amount,member,coupon,expected", [
    (8000, 1, 1, 1600.0),
    (8000, 0, 0, 800.0),
    (3000, 1, 0, 0.0),
    (3000, 0, 1, 500.0),
])
def test_oat_cases(amount, member, coupon, expected):
    assert calculate_discount(amount, member, coupon) == expected
