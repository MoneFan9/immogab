import json
import pytest
from decimal import Decimal
from unittest.mock import patch, MagicMock
from payments.utils.commission import calculate_revenue_split
from payments.gateways.mock import MockPaymentGateway
from payments.tasks import simulate_payment_webhook

def test_commission_calculation_exact():
    """Verify that 10% commission on 10000 is exactly 1000."""
    total = Decimal("10000")
    commission, host_share = calculate_revenue_split(total)

    assert commission == Decimal("1000")
    assert host_share == Decimal("9000")
    assert commission + host_share == total

def test_commission_calculation_rounding():
    """Verify rounding on 10% commission of 9999 (999.9 -> 1000)."""
    total = Decimal("9999")
    commission, host_share = calculate_revenue_split(total)

    # 9999 * 0.10 = 999.9 -> rounded to 1000
    assert commission == Decimal("1000")
    assert host_share == Decimal("8999")
    assert commission + host_share == total

def test_mock_gateway_initiates_pending():
    """Verify that MockPaymentGateway returns a pending status and triggers the task."""
    gateway = MockPaymentGateway()

    with patch("payments.tasks.simulate_payment_webhook.delay") as mock_delay:
        result = gateway.process_payment(amount=5000, currency="XAF", reference="REF123")

        assert result["status"] == "pending"
        assert "transaction_id" in result
        mock_delay.assert_called_once()

@pytest.mark.django_db
def test_async_webhook_simulation(client):
    """
    Verify the asynchronous simulation flow.
    In testing, CELERY_TASK_ALWAYS_EAGER=True, so it runs synchronously.
    """
    gateway = MockPaymentGateway()
    amount = 5000
    reference = "REF-ASYNC"

    # We need to mock the external request since we don't have a server running in pytest
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200

        result = gateway.process_payment(amount=amount, currency="XAF", reference=reference)
        transaction_id = result["transaction_id"]

        # In eager mode, the task should have run and called requests.post
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        payload = kwargs["json"]

        assert payload["status"] == "success"
        assert payload["transaction_id"] == transaction_id
        assert payload["amount"] == amount
        assert payload["reference"] == reference

@pytest.mark.django_db
def test_webhook_view_updates_gateway(client):
    """Verify that the webhook endpoint correctly processes the payload via the gateway."""
    payload = {
        "status": "success",
        "transaction_id": "test-tx-id",
        "amount": 5000,
        "currency": "XAF",
        "reference": "test-ref"
    }

    response = client.post(
        "/api/payments/webhook/mock/",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["transaction_id"] == "test-tx-id"
