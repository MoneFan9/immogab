from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount, currency, phone_number, reference):
        """
        Initiates a payment request.
        For mobile money, this typically triggers a USSD push or returns an instruction.
        """
        pass

    @abstractmethod
    def verify_otp(self, transaction_id, otp):
        """
        Verifies a transaction using an OTP (One-Time Password) if required by the provider.
        """
        pass

    @abstractmethod
    def handle_webhook(self, data, headers):
        """
        Processes asynchronous notifications from the payment provider.
        """
        pass

    @abstractmethod
    def get_status(self, transaction_id):
        """
        Polls the current status of a transaction.
        """
        pass
