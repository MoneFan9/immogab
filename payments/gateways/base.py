from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    """
    Abstract interface for all payment providers (Mobile Money, Cards, etc.)
    """

    @abstractmethod
    def initiate_payment(self, amount, currency, reference, customer_info):
        """
        Starts a transaction. Returns provider-specific data (e.g., redirect URL, transaction ID).
        """
        pass

    @abstractmethod
    def confirm_otp(self, transaction_id, otp):
        """
        Confirms a transaction using an OTP (common in Mobile Money flows).
        """
        pass

    @abstractmethod
    def verify_payment(self, transaction_id):
        """
        Polls the provider to verify the final status of a transaction.
        """
        pass

    @abstractmethod
    def handle_webhook(self, payload, signature=None):
        """
        Processes an asynchronous notification from the provider.
        """
        pass

    @abstractmethod
    def parse_webhook_payload(self, payload, signature=None):
        """
        Standardizes provider-specific webhook data into a WebhookPayload object.
        """
        pass
