from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference, customer_id=None):
        """
        Initiates a payment process.
        :param amount: Decimal or int amount to be paid
        :param currency: str, e.g. 'XAF'
        :param reference: str, unique reference for the transaction
        :param customer_id: Optional identifier for the customer
        :return: dict with status and transaction details
        """
        pass
