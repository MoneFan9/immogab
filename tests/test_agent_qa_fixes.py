import pytest
import requests
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from immogab.services import check_booking_overlap, search_properties, validate_kyc, call_jeedom_webhook

User = get_user_model()

@pytest.mark.django_db
def test_user_creation_and_kyc():
    # Simulate user creation
    user = User.objects.create_user(username="jules_tester", password="password123")
    user.id_card_number = "GAB-2024-999"

    # Test KYC validation
    validate_kyc(user)
    assert user.is_kyc_verified is True

    # Verify persistence
    user.refresh_from_db()
    assert user.is_kyc_verified is True

def test_check_booking_overlap_invalid_dates():
    start = datetime(2026, 5, 10, 14, 0)
    end = datetime(2026, 5, 10, 10, 0) # End before start

    with pytest.raises(ValueError, match="Start time must be before end time"):
        check_booking_overlap(start, end, [])

def test_double_booking_overlap_logic():
    # Existing booking: 10:00 - 12:00
    b1_start = datetime(2026, 5, 10, 10, 0)
    b1_end = datetime(2026, 5, 10, 12, 0)
    existing = [MagicMock(start_time=b1_start, end_time=b1_end)]

    # Case 1: Overlap at the beginning (09:00 - 11:00)
    assert check_booking_overlap(datetime(2026, 5, 10, 9, 0), datetime(2026, 5, 10, 11, 0), existing) is True

    # Case 2: Overlap at the end (11:00 - 13:00)
    assert check_booking_overlap(datetime(2026, 5, 10, 11, 0), datetime(2026, 5, 10, 13, 0), existing) is True

    # Case 3: Completely inside (10:30 - 11:30)
    assert check_booking_overlap(datetime(2026, 5, 10, 10, 30), datetime(2026, 5, 10, 11, 30), existing) is True

    # Case 4: Completely outside (starts exactly when previous ends)
    assert check_booking_overlap(datetime(2026, 5, 10, 12, 0), datetime(2026, 5, 10, 14, 0), existing) is False

@pytest.mark.django_db
def test_search_properties_filters():
    from properties.models import Property
    Property.objects.create(title="Villa", province="Ogooué-Maritime", property_type="Maison", price_per_day=100000)
    Property.objects.create(title="Terrain 1", province="Estuaire", property_type="Terrain", price_per_day=50000)

    # Test province filter
    res_province = search_properties(province="Ogooué-Maritime")
    assert len(res_province) >= 1
    assert all(p.province == "Ogooué-Maritime" for p in res_province)

    # Test property_type filter
    res_type = search_properties(property_type="Terrain")
    assert len(res_type) >= 1
    assert all(p.property_type == "Terrain" for p in res_type)

@patch("requests.Session.post")
def test_call_jeedom_webhook_malformed_json(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Simulate malformed JSON
    mock_response.json.side_effect = ValueError("No JSON object could be decoded")
    mock_post.return_value = mock_response

    with pytest.raises(ConnectionError, match="Jeedom returned an invalid JSON response"):
        call_jeedom_webhook("http://jeedom.local/api", "cmd", "key")
