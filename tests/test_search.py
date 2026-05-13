import pytest
from rest_framework.test import APIClient
from properties.models import Property

@pytest.mark.django_db
def test_property_search_filtering():
    client = APIClient()

    # Create test data
    Property.objects.create(
        title="Villa Estuaire",
        province="estuaire",
        property_type="villa",
        price_per_hour=10000,
        city="Libreville",
        address="Bord de mer"
    )
    Property.objects.create(
        title="Appartement Maritime",
        province="ogooue_maritime",
        property_type="appartement",
        price_per_hour=5000,
        city="Port-Gentil",
        address="Centre-ville"
    )

    # Test filter by province
    response = client.get('/api/properties/', {'province': 'estuaire'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Villa Estuaire"

    # Test filter by type
    response = client.get('/api/properties/', {'property_type': 'appartement'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Appartement Maritime"

    # Test price filtering
    response = client.get('/api/properties/', {'min_price': 6000})
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Villa Estuaire"

    # Test search
    response = client.get('/api/properties/', {'search': 'Maritime'})
    assert len(response.data) == 1
    assert response.data[0]['title'] == "Appartement Maritime"
