from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount, currency, reference, phone_number=None):
        """
        Initiates a payment request.
        """
        pass

    @abstractmethod
    def process_otp(self, transaction_id, otp_code):
        """
        Processes an OTP for payment validation if required.
        """
        pass

    @abstractmethod
    def handle_webhook(self, data, headers):
        """
        Handles incoming webhook callbacks from the payment provider.
        """
        pass
