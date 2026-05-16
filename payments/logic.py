from decimal import Decimal, ROUND_HALF_UP

def calculate_revenue_split(total_amount, commission_rate):
    """
    Calculates the revenue split between ImmoGab (commission) and the Host.
    Ensures mathematical correctness: total = commission + host.
    Rounding is handled for XAF (CFA Franc), which usually doesn't have decimals.
    """
    if isinstance(total_amount, (int, float)):
        total_amount = Decimal(str(total_amount))
    if isinstance(commission_rate, (int, float)):
        commission_rate = Decimal(str(commission_rate))

    # Calculate commission and round to 0 decimal places (XAF standard)
    commission = (total_amount * commission_rate).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    # Host gets the remainder to ensure total_amount == commission + host
    host = total_amount - commission

    return {
        'total': total_amount,
        'commission': commission,
        'host': host,
        'rate': commission_rate
    }
