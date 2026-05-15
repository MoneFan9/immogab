import pytest
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from immogab.services import (
    search_properties,
    validate_kyc,
    check_booking_overlap,
    MockPaymentGateway,
    call_jeedom_webhook
)

@pytest.fixture
def test_user():
    user = MagicMock()
    user.id_card_number = "CNI-987654321"
    user.is_kyc_verified = False
    return user

@patch("requests.post")
def test_full_e2e_journey_simulation(mock_post, test_user):
    # 1. Search for a property in Libreville
    properties = search_properties(query="Libreville", province="Estuaire")
    assert len(properties) > 0
    selected_property = properties[0]
    assert "Libreville" in selected_property.location

    # 2. KYC Validation
    assert validate_kyc(test_user) is True
    assert test_user.is_kyc_verified is True

    # 3. Booking Overlap Check
    start = datetime.now() + timedelta(days=1)
    end = start + timedelta(hours=2)
    # Simulate existing bookings
    existing = [
        MagicMock(start_time=start + timedelta(hours=5), end_time=start + timedelta(hours=7))
    ]
    assert check_booking_overlap(start, end, existing) is False

    # 4. Payment Simulation
    gateway = MockPaymentGateway()
    payment = gateway.process_payment(amount=15000, currency="XAF", reference="BK-999")
    assert payment["status"] == "success"
    assert "transaction_id" in payment

    # 5. Jeedom Signal
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
    mock_post.return_value = mock_response

    jeedom_call = call_jeedom_webhook("http://jeedom.local", "lock-1", "key-xyz")
    assert jeedom_call is True

    # Verify JSON-RPC payload
    _, kwargs = mock_post.call_args
    assert kwargs["json"]["jsonrpc"] == "2.0"
    assert kwargs["json"]["method"] == "cmd::exec"

def test_journey_failure_invalid_dates():
    start = datetime.now() + timedelta(days=1)
    end = start - timedelta(hours=1) # End before start
    with pytest.raises(ValueError, match="End time must be after start time"):
        check_booking_overlap(start, end, [])

def test_journey_failure_kyc_missing():
    user = MagicMock()
    user.id_card_number = None
    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)

@patch("requests.post")
def test_journey_failure_jeedom_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "jsonrpc": "2.0",
        "error": {"message": "Invalid command"},
        "id": 1
    }
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom RPC error: Invalid command"):
        call_jeedom_webhook("http://jeedom.local", "bad-cmd", "key")
