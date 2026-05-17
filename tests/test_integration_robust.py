import pytest
import requests
from datetime import datetime
from unittest.mock import patch, MagicMock
from immogab.services import (
    validate_kyc,
    check_booking_overlap,
    call_jeedom_webhook,
    search_properties
)
from properties.models import Property

class PersistentMock:
    """A mock that can simulate DB persistence."""
    def __init__(self, **kwargs):
        self._data = kwargs
        self.saved_data = {}
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        # Capture current state to simulate DB save
        self.saved_data = {
            'is_kyc_verified': getattr(self, 'is_kyc_verified', False),
            'id_card_number': getattr(self, 'id_card_number', None)
        }

@pytest.mark.django_db
def test_e2e_robust_journey_and_failures():
    # Pre-create a property for search
    Property.objects.create(
        title="House in Libreville",
        city="Libreville",
        province="estuaire",
        property_type="maison"
    )

    # 1. Search for a house in Libreville (Real ORM)
    properties = search_properties(query="Libreville")
    assert len(properties) > 0
    target_property = properties[0]
    assert target_property.city == "Libreville"

    # 2. KYC Validation with Persistence Check
    # Using PersistentMock to verify that .save() is called and changes are intended for persistence
    user = PersistentMock(id_card_number="GAB-999", is_kyc_verified=False)

    validate_kyc(user)

    # Check if .save() was called and persisted the correct state
    assert user.is_kyc_verified is True
    assert user.saved_data.get('is_kyc_verified') is True

    # 3. Booking Overlap with Edge Case (Invalid Dates)
    # Start >= End should be handled
    start = datetime(2026, 12, 25, 15, 0)
    end = datetime(2026, 12, 25, 14, 0) # End before start

    with pytest.raises(ValueError, match="Start time must be before end time"):
        check_booking_overlap(start, end, [])

    # 4. Jeedom Webhook with Robustness Check (Invalid JSON Response)
    with patch("requests.Session.post") as mock_post:
        # Simulate a 200 OK but with malformed JSON
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")
        mock_post.return_value = mock_response

        # We expect it to be wrapped in a ConnectionError
        with pytest.raises(ConnectionError, match="Jeedom returned an invalid JSON response"):
             call_jeedom_webhook("http://jeedom", "cmd", "key")

def test_booking_overlap_logic_edge_cases():
    # Case: Start time equals End time
    start = datetime(2026, 1, 1, 10, 0)
    end = datetime(2026, 1, 1, 10, 0)
    existing = [MagicMock(start_time=datetime(2026, 1, 1, 9, 0), end_time=datetime(2026, 1, 1, 11, 0))]

    # This should raise a ValueError
    with pytest.raises(ValueError, match="Start time must be before end time"):
        check_booking_overlap(start, end, existing)
