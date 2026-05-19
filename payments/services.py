from .interfaces import PaymentGateway
from .models import PaymentTransaction
from .tasks import simulate_mobile_money_webhook
import uuid

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation of a mobile money gateway in Gabon (Airtel/Moov).
    Initiates a pending payment and triggers an asynchronous simulation.
    """
    def process_payment(self, booking, amount, currency, provider):
        transaction_id = f"PAY-{uuid.uuid4().hex[:8].upper()}"

        # 1. Create a PENDING payment record
        payment = PaymentTransaction.objects.create(
            booking=booking,
            amount=amount,
            currency=currency,
            transaction_id=transaction_id,
            provider=provider,
            status=PaymentTransaction.PaymentStatus.PENDING
        )

        # 2. Trigger asynchronous simulation (Mobile Money takes time)
        # We pass the payment ID to the task
        simulate_mobile_money_webhook.delay(payment.id)

        return {
            "status": "initiated",
            "payment_id": str(payment.id),
            "reference": transaction_id,
            "message": "Payment initiated, waiting for provider confirmation."
        }
