import uuid
from payments.interfaces import PaymentGateway

class MoovMoneyGateway(PaymentGateway):
    def initiate_payment(self, amount, currency, phone_number, reference):
        # In a real scenario, this would call Moov Gabon's (Flooz) API
        return {
            "status": "pending",
            "provider": "moov",
            "transaction_id": str(uuid.uuid4()),
            "message": f"Waiting for Moov Money confirmation on {phone_number}"
        }

    def verify_otp(self, transaction_id, otp):
        # Moov often relies on PIN on the phone, but some web flows use OTP
        return {"status": "success", "transaction_id": transaction_id}

    def handle_webhook(self, data, headers):
        # logic to parse Moov specific webhook format
        status = "SUCCESS" if data.get("result") == "completed" else "FAILED"
        return {
            "status": status,
            "external_reference": data.get("moov_trans_id"),
            "transaction_id": data.get("client_reference")
        }

    def get_status(self, transaction_id):
        # Query Moov API for transaction status
        return {"status": "SUCCESS", "transaction_id": transaction_id}
