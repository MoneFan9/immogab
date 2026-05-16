from .interfaces import PaymentGateway
from .models import Payment
from .tasks import simulate_mobile_money_webhook
import uuid

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation of a mobile money gateway in Gabon (Airtel/Moov).
    Initiates a pending payment and triggers an asynchronous simulation.
    """
    def process_payment(self, booking, amount, currency, provider):
        reference = f"PAY-{uuid.uuid4().hex[:8].upper()}"

        # 1. Create a PENDING payment record
        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            reference=reference,
            provider=provider,
            status='PENDING'
        )

        # 2. Trigger asynchronous simulation (Mobile Money takes time)
        # We pass the payment ID to the task
        simulate_mobile_money_webhook.delay(payment.id)

        return {
            "status": "initiated",
            "payment_id": str(payment.id),
            "reference": reference,
            "message": "Payment initiated, waiting for provider confirmation."
        }
