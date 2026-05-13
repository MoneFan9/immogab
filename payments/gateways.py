import uuid
from abc import ABC, abstractmethod
from datetime import datetime

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference):
        """
        Process a payment through the gateway.
        """
        pass

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation of a payment gateway that simulates success.
    """
    def process_payment(self, amount, currency, reference):
        # Simulate a successful transaction
        return {
            "status": "success",
            "transaction_id": str(uuid.uuid4()),
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": datetime.now().isoformat()
        }
