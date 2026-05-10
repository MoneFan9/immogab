import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.username = "testuser"
    user.is_kyc_verified = False
    return user

@pytest.fixture
def mock_property():
    prop = MagicMock()
    prop.id = 1
    prop.name = "Villa Gabonaise"
    return prop
