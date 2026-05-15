import pytest
from immogab.services import MockPaymentGateway, PaymentGateway

def test_mock_payment_gateway_process_payment():
    gateway = MockPaymentGateway()
    amount = 10000
    currency = "XAF"
    reference = "TEST-REF-123"

    result = gateway.process_payment(amount, currency, reference)

    assert result["status"] == "success"
    assert "transaction_id" in result
    assert result["amount"] == amount
    assert result["currency"] == currency
    assert result["reference"] == reference
    assert "timestamp" in result

def test_gateway_is_instance_of_abstract_base():
    gateway = MockPaymentGateway()
    assert isinstance(gateway, PaymentGateway)

def test_abstract_gateway_cannot_be_instantiated():
    with pytest.raises(TypeError):
        PaymentGateway()
