from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings

def calculate_revenue_split(total_amount):
    """
    Calculates the split between ImmoGab (commission) and the Host (owner).

    :param total_amount: The total amount paid by the guest (Decimal or float).
    :return: A tuple of (immogab_commission, host_payout) as Decimals.
    """
    if not isinstance(total_amount, Decimal):
        total_amount = Decimal(str(total_amount))

    commission_rate = Decimal(getattr(settings, 'IMMOGAB_COMMISSION_PERCENTAGE', '15.0')) / Decimal('100')

    # ImmoGab Commission
    immogab_commission = (total_amount * commission_rate).quantize(Decimal('1.'), rounding=ROUND_HALF_UP)

    # Host Payout
    host_payout = total_amount - immogab_commission

    return immogab_commission, host_payout
