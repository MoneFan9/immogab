from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount, currency, phone_number, reference):
        """
        Initiates a payment request (e.g., USSD Push).
        Returns a dictionary with status and transaction details.
        """
        pass

    @abstractmethod
    def handle_webhook(self, data, headers):
        """
        Processes provider-specific webhook data.
        Returns a dictionary with normalized status and references.
        """
        pass

    @abstractmethod
    def verify_otp(self, transaction_id, otp):
        """
        Verifies an OTP for transactions that require it.
        """
        pass

    @abstractmethod
    def get_status(self, transaction_id):
        """
        Queries the provider for the current status of a transaction.
        """
        pass

    def process_payment(self, booking, amount, currency, provider):
        """
        Legacy/High-level method for immediate processing (e.g., for Mocks).
        """
        pass
