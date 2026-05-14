import uuid
from datetime import datetime
from .base import PaymentGateway
from ..tasks import simulate_payment_webhook

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation for testing purposes.
    Simulates a mobile money payment in Gabon (Airtel/Moov).
    """
    def process_payment(self, amount, currency, reference):
        transaction_id = str(uuid.uuid4())

        # Trigger asynchronous simulation of success
        # In a real scenario, the provider would call our webhook after some time.
        simulate_payment_webhook.delay(
            transaction_id=transaction_id,
            amount=amount,
            currency=currency,
            reference=reference
        )

        return {
            "status": "pending",
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": datetime.now().isoformat(),
            "message": "Payment initiated. Waiting for mobile confirmation."
        }

    def handle_webhook(self, payload):
        # Implementation for handling the simulated webhook
        return {
            "status": "success",
            "transaction_id": payload.get("transaction_id"),
            "reference": payload.get("reference")
        }
