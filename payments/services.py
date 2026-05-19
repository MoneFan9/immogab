from .models import PaymentTransaction
from .factory import get_payment_gateway
import uuid

def initiate_mobile_money_payment(booking, amount, currency, provider, phone_number):
    """
    Service to initiate a mobile money payment.
    Creates a PaymentTransaction record and calls the provider's gateway.
    """
    gateway = get_payment_gateway(provider)

    reference = f"PAY-{uuid.uuid4().hex[:8].upper()}"

    # 1. Initiate with provider
    result = gateway.initiate_payment(amount, currency, phone_number, reference)

    # 2. Create local transaction record
    PaymentTransaction.objects.create(
        booking=booking,
        amount=amount,
        currency=currency,
        transaction_id=result['transaction_id'],
        provider=provider.upper(),
        phone_number=phone_number,
        status=PaymentTransaction.PaymentStatus.PENDING
    )

    return result
