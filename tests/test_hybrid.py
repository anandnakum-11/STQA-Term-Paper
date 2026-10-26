import pytest
from src.discount_system import calculate_discount

# The existing four representative cases plus threshold boundary cases.
@pytest.mark.parametrize("amount,member,coupon,expected", [
    (8000, 1, 0, 1600.0),
    (8000, 0, 0, 800.0),
    (3000, 0, 1, 500.0),
    (3000, 1, 0, 0.0),
    (5000, 1, 0, 1000.0),  # exact threshold, member
    (5000, 0, 1, 500.0),   # exact threshold, non-member
    (4999, 1, 1, 500.0),   # just below threshold
    (4999, 0, 0, 0.0),     # just below threshold, no coupon
])
def test_hybrid_cases(amount, member, coupon, expected):
    assert calculate_discount(amount, member, coupon) == expected
