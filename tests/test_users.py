import pytest
from unittest.mock import MagicMock
from immogab.services import validate_kyc

@pytest.mark.django_db
def test_user_creation_requires_kyc():
    """
    Simulate user creation and verify KYC requirement.
    """
    user_data = {
        "username": "johndoe",
        "cni_number": "GAB12345",
    }

    # Use a simple class instead of MagicMock for business logic where possible,
    # but here we can just use a simple object as it's not querying the DB yet in validate_kyc
    class SimpleUser:
        def __init__(self, cni_number):
            self.cni_number = cni_number
            self.is_kyc_verified = False

    user = SimpleUser(cni_number=user_data["cni_number"])

    # The service should be able to validate based on cni_number presence
    assert validate_kyc(user) is True
    assert user.is_kyc_verified is True

def test_user_creation_fails_without_id_card():
    class SimpleUser:
        def __init__(self, cni_number):
            self.cni_number = cni_number
            self.is_kyc_verified = False

    user = SimpleUser(cni_number=None)

    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)
