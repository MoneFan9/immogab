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

@pytest.mark.django_db
def test_actual_user_creation_in_db():
    from django.contrib.auth.models import User

    # Create user via Django's User.objects.create_user
    user = User.objects.create_user(
        username="testuser_db",
        password="password123",
        email="test@example.com"
    )

    assert user.id is not None
    assert User.objects.filter(username="testuser_db").exists()

    # Check KYC fails initially because id_card_number is missing on standard User model
    # (In a real app, User model would be customized or have a Profile)
    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)

def test_validate_kyc_missing_attribute():
    # Test robustness with object missing the attribute entirely
    user = object()
    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)
