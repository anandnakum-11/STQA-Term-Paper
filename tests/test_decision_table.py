import pytest
from src.discount_system import calculate_discount

# One representative input for each of the four business rules.
@pytest.mark.parametrize("amount,member,coupon,expected", [
    (8000, 1, 0, 1600.0),  # high amount + member -> 20%
    (8000, 0, 1, 800.0),   # high amount + non-member -> 10%; coupon irrelevant
    (3000, 0, 1, 500.0),  # low amount + coupon -> flat discount
    (3000, 1, 0, 0.0),    # low amount + no coupon -> no discount
])
def test_decision_table_cases(amount, member, coupon, expected):
    assert calculate_discount(amount, member, coupon) == expected
