import uuid
from datetime import datetime
from payments.interfaces import PaymentGateway
from payments.tasks import simulate_mobile_money_callback

class MockPaymentGateway(PaymentGateway):
    """
    Improved Mock implementation for Gabon Mobile Money (Airtel/Moov).
    Simulates the initiation and triggers an asynchronous success callback.
    """
    def process_payment(self, amount, currency, reference, customer_id=None):
        transaction_id = str(uuid.uuid4())

        # In a real scenario, this would call an API like Airtel Money Gabon
        # and return a "PENDING" status while waiting for the user to enter OTP.

        # Trigger the asynchronous simulation of user validation/OTP success.
        simulate_mobile_money_callback.delay(
            transaction_id=transaction_id,
            amount=float(amount),
            currency=currency,
            reference=reference
        )

        return {
            "status": "initiated",
            "message": "Payment initiated. Waiting for OTP validation.",
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": datetime.now().isoformat()
        }
