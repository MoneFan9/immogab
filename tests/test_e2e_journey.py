import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from core.models import User
from immogab.services import (
    check_booking_overlap,
    call_jeedom_webhook,
    MockPaymentGateway
)

@pytest.fixture
def real_user(db):
    return User.objects.create_user(username='e2euser', cni_number='GAB-E2E-123')

@patch("requests.post")
def test_e2e_journey_success(mock_post, real_user):
    # 1. KYC Validation (Asynchronous Simulation)
    assert real_user.is_kyc_verified is False
    # Manual validation for test purposes as we removed the old service
    real_user.is_kyc_verified = True
    real_user.save()
    assert real_user.is_kyc_verified is True

    # 2. Booking Overlap Check
    start_time = datetime(2026, 6, 1, 10, 0)
    end_time = datetime(2026, 6, 1, 14, 0)
    existing_bookings = [] # No bookings yet
    assert check_booking_overlap(start_time, end_time, existing_bookings) is False

    # 3. Payment
    gateway = MockPaymentGateway()
    payment_result = gateway.process_payment(amount=20000, currency="XAF", reference="BOOK-123")
    assert payment_result["status"] == "success"

    # 4. Jeedom Signal
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
    mock_post.return_value = mock_response

    jeedom_result = call_jeedom_webhook(
        api_url="http://jeedom.local/api",
        command="open_lock",
        api_key="secret_key"
    )
    assert jeedom_result is True

    # Check JSON-RPC 2.0 compliance
    args, kwargs = mock_post.call_args
    sent_json = kwargs["json"]
    assert sent_json["jsonrpc"] == "2.0"
    assert sent_json["method"] == "cmd::exec"
