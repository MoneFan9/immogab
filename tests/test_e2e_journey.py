import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import User
from properties.models import Property
from immogab.services import (
    validate_kyc,
    check_booking_overlap,
    call_jeedom_webhook,
    search_properties
)

@pytest.fixture
def db_user(db):
    return User.objects.create_user(
        username="testcustomer",
        password="password",
        id_card_number="123456789"
    )

@pytest.fixture
def db_property(db):
    return Property.objects.create(
        title="Villa à Libreville",
        description="Luxueuse",
        property_type="villa",
        province="estuaire",
        location="Libreville",
        price_per_hour=5000
    )

@pytest.mark.django_db
@patch("requests.post")
def test_e2e_journey_success(mock_post, db_user, db_property):
    # 1. Search for a house in Libreville
    properties = search_properties(query="Libreville")
    assert any(p.location == "Libreville" for p in properties)

    target_property = [p for p in properties if p.location == "Libreville"][0]

    # 2. KYC Validation
    assert validate_kyc(db_user) is True
    assert db_user.is_kyc_verified is True

    # 3. Booking Overlap Check
    start_time = timezone.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=4)
    assert check_booking_overlap(start_time, end_time, target_property.id) is False

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
