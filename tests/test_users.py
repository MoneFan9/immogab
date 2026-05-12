import pytest
from unittest.mock import MagicMock
from immogab.services import validate_kyc

def test_user_creation_requires_kyc():
    """
    Simulate user creation and verify KYC requirement.
    """
    user_data = {
        "username": "johndoe",
        "id_card_number": "GAB12345",
    }

    # Simulate a user model instance
    user = MagicMock()
    user.username = user_data["username"]
    user.id_card_number = user_data["id_card_number"]
    user.is_kyc_verified = False

    # The service should be able to validate based on id_card_number presence
    assert validate_kyc(user) is True
    assert user.is_kyc_verified is True

def test_user_creation_fails_without_id_card():
    user = MagicMock()
    user.username = "baduser"
    user.id_card_number = None
    user.is_kyc_verified = False

    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)

def test_user_creation_fails_with_empty_id_card():
    user = MagicMock()
    user.id_card_number = ""
    user.is_kyc_verified = False

    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)

def test_user_creation_fails_missing_attribute():
    user = object() # Simple object has no id_card_number attribute

    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)
