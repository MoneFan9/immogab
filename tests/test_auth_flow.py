import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_jwt_login_flow(api_client):
    user = User.objects.create_user(username='testuser', password='password123')

    url = reverse('token_obtain_pair')
    response = api_client.post(url, {'username': 'testuser', 'password': 'password123'}, format='json', secure=True)

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_jwt_refresh_flow(api_client):
    user = User.objects.create_user(username='testuser', password='password123')

    login_url = reverse('token_obtain_pair')
    login_response = api_client.post(login_url, {'username': 'testuser', 'password': 'password123'}, format='json', secure=True)
    refresh_token = login_response.data['refresh']

    refresh_url = reverse('token_refresh')
    response = api_client.post(refresh_url, {'refresh': refresh_token}, format='json', secure=True)

    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_user_profile_view(api_client):
    user = User.objects.create_user(username='testuser', email='test@example.com')
    api_client.force_authenticate(user=user)

    url = reverse('user-profile')
    response = api_client.get(url, secure=True)

    assert response.status_code == 200
    assert response.data['username'] == 'testuser'
    assert response.data['email'] == 'test@example.com'
