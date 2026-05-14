from .base import PaymentGateway

class AirtelMoneyGateway(PaymentGateway):
    def initiate_payment(self, amount, currency, reference, phone_number=None):
        # TODO: Implement Airtel Money specific API call
        return {
            "status": "PENDING",
            "provider": "airtel",
            "reference": reference,
            "instructions": "Veuillez valider la transaction sur votre téléphone Airtel Money."
        }

    def process_otp(self, transaction_id, otp_code):
        # TODO: Implement Airtel Money specific OTP verification
        return {"status": "SUCCESS", "transaction_id": transaction_id}

    def handle_webhook(self, data, headers):
        # TODO: Parse Airtel Money specific webhook payload
        return {"status": "PROCESSED"}
