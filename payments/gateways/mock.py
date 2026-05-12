import uuid
from datetime import datetime
from .base import PaymentGateway

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation for development and testing.
    """
    def initiate_payment(self, amount, currency, reference, customer_info):
        return {
            "status": "success",
            "transaction_id": str(uuid.uuid4()),
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": datetime.now().isoformat()
        }

    def confirm_otp(self, transaction_id, otp):
        return {"status": "success", "transaction_id": transaction_id}

    def verify_payment(self, transaction_id):
        return {"status": "success", "transaction_id": transaction_id}

    def handle_webhook(self, payload, signature=None):
        return {"status": "processed", "payload": payload}

    def parse_webhook_payload(self, payload, signature=None):
        from ..webhooks import WebhookPayload
        return WebhookPayload(
            provider="mock",
            transaction_id=payload.get("transaction_id", "mock-id"),
            status=payload.get("status", "success"),
            amount=payload.get("amount", 0.0),
            currency=payload.get("currency", "XAF"),
            reference=payload.get("reference", "mock-ref"),
            raw_data=payload,
            signature=signature
        )
