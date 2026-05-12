from dataclasses import dataclass
from typing import Optional, Any, Dict

@dataclass
class WebhookPayload:
    """
    Standardized structure for incoming payment webhooks.
    """
    provider: str
    transaction_id: str
    status: str
    amount: float
    currency: str
    reference: str
    raw_data: Dict[str, Any]
    signature: Optional[str] = None

def process_webhook(provider_name: str, payload: Dict[str, Any], signature: Optional[str] = None):
    """
    Generic entry point for webhook processing.
    """
    from .factory import PaymentGatewayFactory

    gateway = PaymentGatewayFactory.get_gateway(provider_name)

    # Standardize the payload
    webhook_data = gateway.parse_webhook_payload(payload, signature)

    # Process using standardized data
    result = gateway.handle_webhook(webhook_data.raw_data, webhook_data.signature)

    # In a real implementation, this would also update the Booking/Payment status in DB
    # using webhook_data fields like status, transaction_id, reference.
    return result
