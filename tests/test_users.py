import pytest
from core.models import User

@pytest.mark.django_db
def test_user_creation_requires_kyc():
    """
    Verify KYC requirement using the real User model.
    """
    user = User.objects.create_user(username='johndoe', cni_number='GAB12345')
    assert user.is_kyc_verified is False

    # Simulate validation (as it would happen in the task)
    user.is_kyc_verified = True
    user.save()

    assert user.is_kyc_verified is True

@pytest.mark.django_db
def test_user_creation_without_cni():
    user = User.objects.create_user(username='baduser')
    assert user.cni_number is None
    assert user.is_kyc_verified is False
