import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from immogab.services import (
    validate_kyc,
    check_booking_overlap,
    call_jeedom_webhook,
    # These will be implemented next
)

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id_card_number = "123456789"
    user.is_kyc_verified = False
    return user

@pytest.fixture
def mock_property():
    prop = MagicMock()
    prop.id = 1
    prop.title = "Villa à Libreville"
    prop.location = "Libreville"
    prop.hourly_rate = 5000
    return prop

@pytest.mark.django_db
@patch("requests.Session.post")
def test_e2e_journey_success(mock_post, mock_user, mock_property):
    # 1. Search for a house in Libreville
    from properties.models import Property
    Property.objects.create(
        title="Villa à Libreville",
        description="Une belle villa",
        property_type="MAISON",
        province="Estuaire",
        city="Libreville",
        neighborhood="Sablière"
    )
    # We expect a search_properties function to exist
    from immogab.services import search_properties
    properties = search_properties(query="Libreville")
    assert any(p.city == "Libreville" for p in properties)

    target_property = [p for p in properties if p.city == "Libreville"][0]

    # 2. KYC Validation
    assert validate_kyc(mock_user) is True
    assert mock_user.is_kyc_verified is True

    # 3. Booking Overlap Check
    start_time = datetime(2026, 6, 1, 10, 0)
    end_time = datetime(2026, 6, 1, 14, 0)
    existing_bookings = [] # No bookings yet
    assert check_booking_overlap(start_time, end_time, existing_bookings) is False

    # 4. Payment (Fictitious)
    # We expect a PaymentGateway and MockPaymentGateway
    from immogab.services import MockPaymentGateway
    # Create a real user for legacy support in MockPaymentGateway
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.get_or_create(id=1, defaults={'username': 'legacy_user'})

    with patch("payments.services.simulate_mobile_money_webhook.delay"):
        gateway = MockPaymentGateway()
        payment_result = gateway.process_payment(amount=20000, currency="XAF", reference="BOOK-123")
        assert payment_result["status"] == "initiated"

    # 5. Jeedom Signal
    # Mocking successful Jeedom response
    mock_response = MagicMock()
    mock_response.status_code = 200
    # JSON-RPC 2.0 response format
    mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
    mock_post.return_value = mock_response

    jeedom_result = call_jeedom_webhook(
        api_url="http://jeedom.local/api",
        command="open_lock",
        api_key="secret_key"
    )
    assert jeedom_result is True

    # Check if the signal sent followed JSON-RPC 2.0
    # Note: requests.Session.post is called inside call_jeedom_webhook
    args, kwargs = mock_post.call_args
    sent_json = kwargs["json"]
    assert sent_json["jsonrpc"] == "2.0"
    assert sent_json["method"] == "cmd::exec" # Standard Jeedom method for commands
    assert sent_json["params"]["apikey"] == "secret_key"
    assert sent_json["params"]["id"] == "open_lock"
