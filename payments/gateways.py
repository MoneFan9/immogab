from .interfaces import PaymentGateway
from .models import PaymentTransaction
from .factory import get_payment_gateway
import uuid

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation of a mobile money gateway.
    Initiates a pending payment and can be used to simulate flows.
    """
    def initiate_payment(self, amount, currency, phone_number, reference):
        transaction_id = f"MOCK-{uuid.uuid4().hex[:8].upper()}"
        return {
            "status": "pending",
            "transaction_id": transaction_id,
            "provider": "mock",
            "message": "Mock payment initiated."
        }

    def handle_webhook(self, data, headers):
        return {
            "status": "SUCCESS",
            "transaction_id": data.get("transaction_id"),
            "external_reference": f"EXT-{uuid.uuid4().hex[:6].upper()}"
        }

    def verify_otp(self, transaction_id, otp):
        return {"status": "success", "transaction_id": transaction_id}

    def get_status(self, transaction_id):
        return {"status": "SUCCESS", "transaction_id": transaction_id}

    def process_payment(self, booking, amount, currency, provider):
        """
        Legacy/High-level method for immediate processing.
        Useful for synchronous tests or simple mock flows.
        """
        from bookings.services import synchronize_payment_status

        transaction_id = f"MOCK-SYNC-{uuid.uuid4().hex[:8].upper()}"

        transaction = PaymentTransaction.objects.create(
            booking=booking,
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            status=PaymentTransaction.PaymentStatus.SUCCESS,
            provider=provider
        )

        synchronize_payment_status(booking, "SUCCESS")

        return {
            "status": "success",
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency
        }
