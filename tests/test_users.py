import pytest
from core.models import User
from immogab.services import validate_kyc

@pytest.mark.django_db
def test_user_creation_requires_kyc():
    """
    Simulate user creation and verify KYC requirement.
    """
    user = User.objects.create_user(
        username="johndoe",
        id_card_number="GAB12345",
    )

    # The service should be able to validate based on id_card_number presence
    assert validate_kyc(user) is True
    assert user.is_kyc_verified is True

@pytest.mark.django_db
def test_user_creation_fails_without_id_card():
    user = User.objects.create_user(
        username="baduser",
        id_card_number=None,
    )

    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)
