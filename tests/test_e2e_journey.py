import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from immogab.services import (
    validate_kyc,
    check_booking_overlap,
    call_jeedom_webhook,
)

class SimpleUser:
    def __init__(self, cni_number=None, is_kyc_verified=False):
        self.cni_number = cni_number
        self.is_kyc_verified = is_kyc_verified

class SimpleProperty:
    def __init__(self, location, title="Test"):
        self.location = location
        self.title = title

@pytest.fixture
def mock_user():
    return SimpleUser(cni_number="123456789")

@pytest.fixture
def mock_property():
    return SimpleProperty(location="Libreville", title="Villa à Libreville")

@pytest.mark.django_db
@patch("requests.post")
def test_e2e_journey_success(mock_post, mock_user, mock_property):
    # 1. Search for a house in Libreville
    from properties.models import Property
    from core.models import User
    from immogab.services import search_properties

    owner = User.objects.create_user(username="owner")
    Property.objects.create(title="Villa à Libreville", location="Libreville", province="Estuaire", type="Maison", owner=owner)

    properties = search_properties(query="Libreville")
    assert any(p.location == "Libreville" for p in properties)

    target_property = [p for p in properties if p.location == "Libreville"][0]

    # 2. KYC Validation
    assert validate_kyc(mock_user) is True
    assert mock_user.is_kyc_verified is True

    # 3. Booking Overlap Check
    start_time = datetime(2026, 6, 1, 10, 0)
    end_time = datetime(2026, 6, 1, 14, 0)

    class SimpleBooking:
        def __init__(self, start, end):
            self.start_time = start
            self.end_time = end

    existing_bookings = [] # No bookings yet
    assert check_booking_overlap(start_time, end_time, existing_bookings) is False

    # 4. Payment (Fictitious)
    from immogab.services import MockPaymentGateway
    gateway = MockPaymentGateway()
    payment_result = gateway.process_payment(amount=20000, currency="XAF", reference="BOOK-123")
    assert payment_result["status"] == "success"

    # 5. Jeedom Signal
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

    args, kwargs = mock_post.call_args
    sent_json = kwargs["json"]
    assert sent_json["jsonrpc"] == "2.0"
    assert sent_json["method"] == "cmd::exec"
    assert sent_json["params"]["apikey"] == "secret_key"
    assert sent_json["params"]["id"] == "open_lock"
