from .base import PaymentGateway

class AirtelMoneyGateway(PaymentGateway):
    """
    Gateway implementation for Airtel Money Gabon.
    """
    def initiate_payment(self, amount, currency, reference, customer_info):
        # Implementation for Airtel Money API call
        return {"status": "pending", "provider": "airtel", "transaction_id": "airtel-t-123"}

    def confirm_otp(self, transaction_id, otp):
        # Implementation for OTP validation via Airtel API
        return {"status": "success", "transaction_id": transaction_id}

    def verify_payment(self, transaction_id):
        # Implementation for transaction status inquiry
        return {"status": "success", "transaction_id": transaction_id}

    def handle_webhook(self, payload, signature=None):
        # Parse and validate Airtel webhook payload
        return {"status": "processed", "reference": payload.get("ref")}

    def parse_webhook_payload(self, payload, signature=None):
        from ..webhooks import WebhookPayload
        return WebhookPayload(
            provider="airtel",
            transaction_id=payload.get("txn_id"),
            status=payload.get("status"),
            amount=float(payload.get("amount", 0)),
            currency=payload.get("currency"),
            reference=payload.get("ref"),
            raw_data=payload,
            signature=signature
        )
