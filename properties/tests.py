from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Property

class PropertyAPITests(APITestCase):
    def setUp(self):
        self.prop1 = Property.objects.create(
            title="Appartement de luxe à Akanda",
            description="Bel appartement avec vue sur mer",
            property_type="appartement",
            province="estuaire",
            city="Akanda",
            neighborhood="Angondjé",
            price_per_day=50000,
            price_per_hour=5000
        )
        self.prop2 = Property.objects.create(
            title="Maison à Port-Gentil",
            description="Grande maison familiale",
            property_type="maison",
            province="ogooue_maritime",
            city="Port-Gentil",
            neighborhood="Chic",
            price_per_day=75000,
            price_per_hour=8000
        )
        self.prop3 = Property.objects.create(
            title="Terrain à vendre",
            description="Beau terrain plat",
            property_type="terrain",
            province="estuaire",
            city="Libreville",
            neighborhood="Owendo",
            price_per_day=None,
            price_per_hour=None
        )
        self.list_url = reverse('property-list')

    def test_list_properties(self):
        response = self.client.get(self.list_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_province(self):
        response = self.client.get(self.list_url, {'province': 'estuaire'}, secure=True)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(self.list_url, {'province': 'ogooue_maritime'}, secure=True)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_type(self):
        response = self.client.get(self.list_url, {'property_type': 'maison'}, secure=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Maison à Port-Gentil")

    def test_filter_by_price_range(self):
        # Daily price range
        response = self.client.get(self.list_url, {'min_price_day': 60000}, secure=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Maison à Port-Gentil")

        # Hourly price range
        response = self.client.get(self.list_url, {'max_price_hour': 6000}, secure=True)
        # prop1 (5000) matches, prop2 (8000) does not, prop3 is null
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Appartement de luxe à Akanda")

    def test_search_functionality(self):
        response = self.client.get(self.list_url, {'search': 'luxe'}, secure=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Appartement de luxe à Akanda")

        response = self.client.get(self.list_url, {'search': 'Port-Gentil'}, secure=True)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['city'], "Port-Gentil")

    def test_ordering(self):
        response = self.client.get(self.list_url, {'ordering': 'price_per_day'}, secure=True)
        # Order should be prop1 (50000), prop2 (75000), then prop3 (null)
        # However, SQLite (default for tests) might put NULLs first or last.
        # Let's filter out properties without prices for the ordering test to be deterministic.
        p1_id = self.prop1.id
        p2_id = self.prop2.id

        # We find indices of prop1 and prop2 in the results
        results_ids = [r['id'] for r in response.data if r['price_per_day'] is not None]
        self.assertEqual(results_ids[0], p1_id)
        self.assertEqual(results_ids[1], p2_id)

        response = self.client.get(self.list_url, {'ordering': '-price_per_day'}, secure=True)
        # Order should be prop2 (75000), prop1 (50000), then prop3 (null)
        results_ids = [r['id'] for r in response.data if r['price_per_day'] is not None]
        self.assertEqual(results_ids[0], p2_id)
        self.assertEqual(results_ids[1], p1_id)
