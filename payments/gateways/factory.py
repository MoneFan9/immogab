from .airtel import AirtelMoneyGateway
from .moov import MoovMoneyGateway
from .mock import MockPaymentGateway

class PaymentFactory:
    _gateways = {
        "airtel": AirtelMoneyGateway,
        "moov": MoovMoneyGateway,
        "mock": MockPaymentGateway,
    }

    @classmethod
    def get_gateway(cls, provider_name):
        gateway_class = cls._gateways.get(provider_name.lower())
        if not gateway_class:
            raise ValueError(f"Unknown payment provider: {provider_name}")
        return gateway_class()
