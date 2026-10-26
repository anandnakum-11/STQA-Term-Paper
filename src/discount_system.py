def calculate_discount(amount: float, is_member: int, has_coupon: int) -> float:
    """Reference implementation of the paper's E-commerce Discount System."""
    discount = 0.0
    if amount >= 5000:
        if is_member == 1:
            discount = amount * 0.20
        else:
            discount = amount * 0.10
    else:
        if has_coupon == 1:
            discount = 500.0
        else:
            discount = 0.0
    return discount
