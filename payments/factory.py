from .providers.airtel import AirtelMoneyGateway
from .providers.moov import MoovMoneyGateway

def get_payment_gateway(provider_name):
    """
    Factory function to return the appropriate payment gateway instance.
    """
    provider_key = provider_name.lower()

    if provider_key == 'airtel':
        return AirtelMoneyGateway()
    elif provider_key == 'moov':
        return MoovMoneyGateway()
    else:
        raise ValueError(f"Unsupported payment provider: {provider_name}")
