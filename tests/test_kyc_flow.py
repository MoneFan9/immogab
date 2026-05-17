import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from users.models import KYCDocument
from users.tasks import validate_kyc_documents

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestUserKYC:
    def test_token_claims(self, api_client):
        user = User.objects.create_user(username='testuser', password='password123', id_card_type='CNI')
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {'username': 'testuser', 'password': 'password123'}, secure=True)

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_kyc_submission_triggers_task(self, api_client, mocker):
        user = User.objects.create_user(username='testuser_kyc', password='password123')
        doc = KYCDocument.objects.create(user=user, document='test.jpg')
        assert doc.status == 'PENDING'

    def test_kyc_validation_task_success(self):
        user = User.objects.create_user(username='testuser_val', id_card_number='GAB12345')
        doc = KYCDocument.objects.create(user=user, document='test.jpg')

        validate_kyc_documents(doc.id)

        user.refresh_from_db()
        doc.refresh_from_db()

        assert user.is_kyc_verified is True
        assert doc.status == KYCDocument.Status.VALIDATED

    def test_kyc_validation_task_rejection(self):
        user = User.objects.create_user(username='testuser_rej', id_card_number=None)
        doc = KYCDocument.objects.create(user=user, document='test.jpg')

        validate_kyc_documents(doc.id)

        user.refresh_from_db()
        doc.refresh_from_db()

        assert user.is_kyc_verified is False
        assert doc.status == KYCDocument.Status.REJECTED
        assert "Missing ID card number" in doc.rejection_reason
