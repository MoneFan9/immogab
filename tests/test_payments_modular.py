import pytest
from django.urls import reverse
from payments.providers.airtel import AirtelMoneyGateway
from payments.providers.moov import MoovMoneyGateway
from payments.models import PaymentTransaction
from immogab.services import ModularPaymentAdapter

@pytest.mark.django_db
class TestModularPayments:
    def test_airtel_initiate_payment(self):
        gateway = AirtelMoneyGateway()
        result = gateway.initiate_payment(1000, "XAF", "077000000", "REF123")
        assert result["status"] == "pending"
        assert result["provider"] == "airtel"
        assert "transaction_id" in result

    def test_moov_initiate_payment(self):
        gateway = MoovMoneyGateway()
        result = gateway.initiate_payment(2000, "XAF", "066000000", "REF456")
        assert result["status"] == "pending"
        assert result["provider"] == "moov"
        assert "transaction_id" in result

    def test_modular_adapter(self):
        airtel = AirtelMoneyGateway()
        adapter = ModularPaymentAdapter(airtel, "077112233")
        result = adapter.process_payment(5000, "XAF", "ADAPTER_REF")
        assert result["status"] == "pending"
        assert result["provider"] == "airtel"

    def test_airtel_webhook_processing(self, client):
        # Create a pending transaction
        tx = PaymentTransaction.objects.create(
            transaction_id="TX_AIRTEL_123",
            amount=1000,
            provider="AIRTEL",
            phone_number="077000000"
        )

        url = reverse("mobile_money_webhook", kwargs={"provider": "airtel"})
        payload = {
            "airtel_status": "00",
            "airtel_ref": "AIRTEL_EXTERNAL_789",
            "custom_id": "TX_AIRTEL_123"
        }

        # Use Secure=True to match settings requirement in tests if SECURE_SSL_REDIRECT is true
        response = client.post(url, data=payload, content_type="application/json", secure=True)
        # Still might need a slash redirect
        if response.status_code == 301:
            response = client.post(response.url, data=payload, content_type="application/json", secure=True)

        assert response.status_code == 200

        tx.refresh_from_db()
        assert tx.status == "SUCCESS"
        assert tx.external_reference == "AIRTEL_EXTERNAL_789"

    def test_moov_webhook_processing(self, client):
        # Create a pending transaction
        tx = PaymentTransaction.objects.create(
            transaction_id="TX_MOOV_456",
            amount=2000,
            provider="MOOV",
            phone_number="066000000"
        )

        url = reverse("mobile_money_webhook", kwargs={"provider": "moov"})
        payload = {
            "result": "completed",
            "moov_trans_id": "MOOV_EXTERNAL_001",
            "client_reference": "TX_MOOV_456"
        }

        response = client.post(url, data=payload, content_type="application/json", secure=True)
        if response.status_code == 301:
            response = client.post(response.url, data=payload, content_type="application/json", secure=True)

        assert response.status_code == 200

        tx.refresh_from_db()
        assert tx.status == "SUCCESS"
        assert tx.external_reference == "MOOV_EXTERNAL_001"
