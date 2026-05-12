import pytest
from payments.factory import PaymentGatewayFactory
from payments.gateways.base import PaymentGateway
from payments.gateways.airtel import AirtelMoneyGateway
from payments.gateways.moov import MoovMoneyGateway
from payments.gateways.mock import MockPaymentGateway

def test_payment_gateway_factory_returns_correct_instances():
    airtel = PaymentGatewayFactory.get_gateway("airtel")
    assert isinstance(airtel, AirtelMoneyGateway)

    moov = PaymentGatewayFactory.get_gateway("moov")
    assert isinstance(moov, MoovMoneyGateway)

    mock = PaymentGatewayFactory.get_gateway("mock")
    assert isinstance(mock, MockPaymentGateway)

def test_payment_gateway_factory_case_insensitivity():
    gateway = PaymentGatewayFactory.get_gateway("AIRTEL")
    assert isinstance(gateway, AirtelMoneyGateway)

def test_payment_gateway_factory_invalid_provider():
    with pytest.raises(ValueError, match="Unknown payment provider"):
        PaymentGatewayFactory.get_gateway("unknown")

def test_mock_gateway_initiate_payment():
    gateway = PaymentGatewayFactory.get_gateway("mock")
    response = gateway.initiate_payment(100, "XAF", "REF-1", {"phone": "123"})
    assert response["status"] == "success"
    assert response["amount"] == 100
    assert "transaction_id" in response

def test_airtel_gateway_skeleton():
    gateway = PaymentGatewayFactory.get_gateway("airtel")
    response = gateway.initiate_payment(500, "XAF", "REF-2", {"phone": "456"})
    assert response["status"] == "pending"
    assert response["provider"] == "airtel"

def test_moov_gateway_skeleton():
    gateway = PaymentGatewayFactory.get_gateway("moov")
    response = gateway.initiate_payment(500, "XAF", "REF-3", {"phone": "789"})
    assert response["status"] == "pending"
    assert response["provider"] == "moov"

def test_gateway_interface_compliance():
    # Verify that all concrete gateways implement all abstract methods
    for provider in ["airtel", "moov", "mock"]:
        gateway = PaymentGatewayFactory.get_gateway(provider)
        assert hasattr(gateway, "initiate_payment")
        assert hasattr(gateway, "confirm_otp")
        assert hasattr(gateway, "verify_payment")
        assert hasattr(gateway, "handle_webhook")
