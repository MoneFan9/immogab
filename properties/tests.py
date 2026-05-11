import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from properties.models import Property

@pytest.mark.django_db
class TestPropertySearch:
    @pytest.fixture(autouse=True)
    def setup_data(self):
        Property.objects.create(
            title="Villa Bord de Mer",
            property_type="MAISON",
            province="ESTUAIRE",
            city="Libreville",
            price_per_hour=10000,
            price_per_day=100000
        )
        Property.objects.create(
            title="Appartement Centre-Ville",
            property_type="APPARTEMENT",
            province="ESTUAIRE",
            city="Libreville",
            price_per_hour=5000,
            price_per_day=50000
        )
        Property.objects.create(
            title="Terrain Sablière",
            property_type="TERRAIN",
            province="ESTUAIRE",
            city="Libreville",
            price_per_hour=None,
            price_per_day=None
        )
        Property.objects.create(
            title="Espace Port-Gentil",
            property_type="ESPACE_EVENEMENTIEL",
            province="OGOOUÉ_MARITIME",
            city="Port-Gentil",
            price_per_hour=15000,
            price_per_day=150000
        )

    def test_list_properties(self):
        client = APIClient()
        url = reverse('property-search-list')
        response = client.get(url)
        assert response.status_code == 200
        # Now with pagination
        assert 'results' in response.data
        assert len(response.data['results']) == 4

    def test_filter_by_province(self):
        client = APIClient()
        url = reverse('property-search-list')
        response = client.get(url, {'province': 'OGOOUÉ_MARITIME'})
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Espace Port-Gentil"

    def test_filter_by_type(self):
        client = APIClient()
        url = reverse('property-search-list')
        response = client.get(url, {'property_type': 'MAISON'})
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Villa Bord de Mer"

    def test_filter_by_price_hour(self):
        client = APIClient()
        url = reverse('property-search-list')
        response = client.get(url, {'min_price_hour': 6000, 'max_price_hour': 12000})
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Villa Bord de Mer"

    def test_filter_by_price_day(self):
        client = APIClient()
        url = reverse('property-search-list')
        response = client.get(url, {'max_price_day': 75000})
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Appartement Centre-Ville"
