from .base import PaymentGateway

class MoovMoneyGateway(PaymentGateway):
    def initiate_payment(self, amount, currency, reference, phone_number=None):
        # TODO: Implement Moov Money specific API call
        return {
            "status": "PENDING",
            "provider": "moov",
            "reference": reference,
            "instructions": "Veuillez saisir le code OTP reçu par SMS."
        }

    def process_otp(self, transaction_id, otp_code):
        # TODO: Implement Moov Money specific OTP verification
        return {"status": "SUCCESS", "transaction_id": transaction_id}

    def handle_webhook(self, data, headers):
        # TODO: Parse Moov Money specific webhook payload
        return {"status": "PROCESSED"}
