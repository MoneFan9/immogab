import pytest
from django.urls import reverse
from rest_framework import status
from core.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestKYCAPI:
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_kyc_submission_authenticated(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('kyc_submission')

        # Create a mock file
        mock_file = SimpleUploadedFile("id_card.pdf", b"file_content", content_type="application/pdf")

        data = {
            'cni_number': 'GAB12345',
            'kyc_document': mock_file
        }

        # Use DJANGO_TESTING=True to make Celery task eager
        os.environ['DJANGO_TESTING'] = 'True'

        response = api_client.put(url, data, format='multipart')

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert response.data['message'] == "KYC document submitted. Verification is in progress."

        # Since CELERY_TASK_ALWAYS_EAGER=True (if DJANGO_TESTING=True is handled in settings)
        # the task should have run synchronously.
        self.user.refresh_from_db()
        assert self.user.cni_number == 'GAB12345'
        assert self.user.is_kyc_verified is True

    def test_kyc_submission_unauthenticated(self, api_client):
        url = reverse('kyc_submission')
        response = api_client.put(url, {}, format='multipart')
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED]

    def test_user_profile_view(self, api_client):
        api_client.force_authenticate(user=self.user)
        url = reverse('user_profile')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
        assert response.data['is_kyc_verified'] is False

@pytest.mark.django_db
class TestJWTAuth:
    def test_token_obtain(self, api_client):
        User.objects.create_user(username='authuser', password='authpassword')
        url = reverse('token_obtain_pair')
        data = {
            'username': 'authuser',
            'password': 'authpassword'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
