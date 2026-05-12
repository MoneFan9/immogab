from .gateways.airtel import AirtelMoneyGateway
from .gateways.moov import MoovMoneyGateway
from .gateways.mock import MockPaymentGateway

class PaymentGatewayFactory:
    _gateways = {
        "airtel": AirtelMoneyGateway,
        "moov": MoovMoneyGateway,
        "mock": MockPaymentGateway,
    }

    @classmethod
    def get_gateway(cls, provider_name: str):
        gateway_class = cls._gateways.get(provider_name.lower())
        if not gateway_class:
            raise ValueError(f"Unknown payment provider: {provider_name}")
        return gateway_class()
