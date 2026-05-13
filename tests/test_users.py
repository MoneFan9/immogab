import pytest
from dataclasses import dataclass, field
from immogab.services import validate_kyc

@dataclass
class UserMock:
    username: str
    id_card_number: str = None
    is_kyc_verified: bool = False
    metadata: dict = field(default_factory=dict)

def test_user_creation_and_kyc_flow():
    """
    Simulate full user creation and KYC verification flow.
    """
    # 1. User registers
    user = UserMock(username="gabon_traveler")
    assert user.is_kyc_verified is False

    # 2. User submits ID card
    user.id_card_number = "CNI-741-2026"

    # 3. System validates KYC
    result = validate_kyc(user)

    assert result is True
    assert user.is_kyc_verified is True

def test_kyc_fails_on_empty_id():
    user = UserMock(username="bad_user", id_card_number="")
    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)

def test_kyc_fails_on_whitespace_id():
    user = UserMock(username="sneaky_user", id_card_number="   ")
    # We should update services.py to handle this edge case
    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)

def test_kyc_missing_attribute():
    @dataclass
    class MinimalUser:
        username: str
        # missing id_card_number

    user = MinimalUser(username="incomplete")
    with pytest.raises(ValueError, match="ID card is required for KYC"):
        validate_kyc(user)
