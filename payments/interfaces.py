from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, booking, amount, currency, provider):
        pass

class ModularPaymentGateway(ABC):
    @abstractmethod
    def initiate_payment(self, amount, currency, phone_number, reference):
        pass

    @abstractmethod
    def verify_otp(self, transaction_id, otp):
        pass

    @abstractmethod
    def handle_webhook(self, data, headers):
        pass

    @abstractmethod
    def process_payment(self, booking, amount, currency, provider):
        pass
