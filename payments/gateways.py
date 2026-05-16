from .interfaces import PaymentGateway
import uuid
from datetime import datetime
from .models import PaymentTransaction
from bookings.services import synchronize_payment_status

class MockPaymentGateway(PaymentGateway):
    def process_payment(self, booking, amount, currency="XAF"):
        # Simulate payment processing
        transaction_id = str(uuid.uuid4())

        # In a real mock, we might want to simulate success/failure
        # For now, let's assume success
        transaction = PaymentTransaction.objects.create(
            booking=booking,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            status=PaymentTransaction.PaymentStatus.SUCCESS,
            provider="Mock"
        )

        synchronize_payment_status(booking, "SUCCESS")

        return {
            "status": "success",
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "timestamp": datetime.now().isoformat()
        }
