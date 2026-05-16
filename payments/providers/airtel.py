import uuid
from datetime import datetime
from payments.interfaces import PaymentGateway

class AirtelMoneyGateway(PaymentGateway):
    def initiate_payment(self, amount, currency, phone_number, reference):
        # In a real scenario, this would call Airtel Gabon's API
        return {
            "status": "pending",
            "provider": "airtel",
            "transaction_id": str(uuid.uuid4()),
            "message": "USSD push sent to " + phone_number
        }

    def verify_otp(self, transaction_id, otp):
        # Airtel might use OTP for some flows
        return {"status": "success", "transaction_id": transaction_id}

    def handle_webhook(self, data, headers):
        # logic to parse Airtel specific webhook format
        return {
            "status": "success" if data.get("airtel_status") == "00" else "failed",
            "external_reference": data.get("airtel_ref"),
            "transaction_id": data.get("custom_id")
        }

    def get_status(self, transaction_id):
        return {"status": "success", "transaction_id": transaction_id}
