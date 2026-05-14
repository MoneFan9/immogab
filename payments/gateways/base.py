from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference):
        """
        Initiates the payment process.
        Returns a dictionary with transaction details.
        """
        pass

    @abstractmethod
    def handle_webhook(self, payload):
        """
        Processes a webhook notification from the payment provider.
        """
        pass
