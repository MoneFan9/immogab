import uuid
from django.utils import timezone
from .base import PaymentGateway

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation that validates automatically.
    """
    def initiate_payment(self, amount, currency, reference, phone_number=None):
        return {
            "status": "success",
            "transaction_id": str(uuid.uuid4()),
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": timezone.now().isoformat()
        }

    def process_otp(self, transaction_id, otp_code):
        return {"status": "SUCCESS", "transaction_id": transaction_id}

    def handle_webhook(self, data, headers):
        return {"status": "PROCESSED"}
