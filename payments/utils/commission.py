from decimal import Decimal, ROUND_HALF_UP

# ImmoGab standard commission (e.g., 10%)
IMMOGAB_COMMISSION_RATE = Decimal("0.10")

def calculate_revenue_split(total_amount, commission_rate=IMMOGAB_COMMISSION_RATE):
    """
    Calculates the split between ImmoGab and the host.
    Uses Decimal for mathematical correctness.

    Returns:
        tuple: (immogab_commission, host_share)
    """
    if not isinstance(total_amount, Decimal):
        total_amount = Decimal(str(total_amount))

    immogab_commission = (total_amount * commission_rate).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    host_share = total_amount - immogab_commission

    return immogab_commission, host_share
