import pytest
from users.models import User
from properties.models import Property

@pytest.mark.django_db
def test_create_user_with_kyc():
    user = User.objects.create_user(
        username="testuser",
        id_card_number="123456789",
        id_card_type="CNI"
    )
    assert user.username == "testuser"
    assert user.id_card_number == "123456789"
    assert user.id_card_type == "CNI"
    assert not user.is_kyc_verified

@pytest.mark.django_db
def test_create_property():
    prop = Property.objects.create(
        title="Villa Test",
        description="A nice test villa",
        property_type="MAISON",
        province="ESTUAIRE",
        city="Libreville",
        neighborhood="Akanda",
        price_per_day=50000
    )
    assert prop.title == "Villa Test"
    assert prop.province == "ESTUAIRE"
    assert prop.property_type == "MAISON"
