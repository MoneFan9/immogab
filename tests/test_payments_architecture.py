import pytest
from rest_framework import status
from django.urls import reverse
from payments.gateways.factory import PaymentFactory
from payments.gateways.airtel import AirtelMoneyGateway
from payments.gateways.moov import MoovMoneyGateway
from payments.gateways.mock import MockPaymentGateway

def test_payment_factory_success():
    assert isinstance(PaymentFactory.get_gateway("airtel"), AirtelMoneyGateway)
    assert isinstance(PaymentFactory.get_gateway("moov"), MoovMoneyGateway)
    assert isinstance(PaymentFactory.get_gateway("mock"), MockPaymentGateway)

def test_payment_factory_case_insensitive():
    assert isinstance(PaymentFactory.get_gateway("AIRTEL"), AirtelMoneyGateway)

def test_payment_factory_failure():
    with pytest.raises(ValueError, match="Unknown payment provider"):
        PaymentFactory.get_gateway("invalid_provider")

@pytest.mark.django_db
def test_webhook_routing_success(client):
    url = reverse('payment_webhook', kwargs={'provider': 'mock'})
    response = client.post(url, data={'test': 'data'}, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"status": "PROCESSED"}

@pytest.mark.django_db
def test_webhook_routing_invalid_provider(client):
    url = reverse('payment_webhook', kwargs={'provider': 'unknown'})
    response = client.post(url, data={}, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data

def test_gateways_implement_interface():
    providers = ["airtel", "moov", "mock"]
    for p in providers:
        gw = PaymentFactory.get_gateway(p)
        assert hasattr(gw, "initiate_payment")
        assert hasattr(gw, "process_otp")
        assert hasattr(gw, "handle_webhook")
