import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User, KYCDocument
from users.tasks import validate_kyc_documents

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestUserKYC:
    def test_token_claims(self, api_client):
        user = User.objects.create_user(username='testuser', password='password123', id_card_type='CNI')
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {'username': 'testuser', 'password': 'password123'})

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

        # In a real test we'd decode the token, but here we can check the custom serializer logic via unit test if needed.

    def test_kyc_submission_triggers_task(self, api_client, mocker):
        mock_delay = mocker.patch('users.tasks.validate_kyc_documents.delay')
        user = User.objects.create_user(username='testuser', password='password123')
        api_client.force_authenticate(user=user)

        url = reverse('kyc_submit')
        file = SimpleUploadedFile("id_card.jpg", b"file_content", content_type="image/jpeg")
        response = api_client.post(url, {'document': file}, format='multipart')

        assert response.status_code == status.HTTP_201_CREATED
        assert KYCDocument.objects.filter(user=user).count() == 1
        mock_delay.assert_called_once()

    def test_kyc_validation_task_success(self):
        user = User.objects.create_user(username='testuser', id_card_number='GAB12345')
        doc = KYCDocument.objects.create(user=user, document='test.jpg')

        validate_kyc_documents(doc.id)

        user.refresh_from_db()
        doc.refresh_from_db()

        assert user.is_kyc_verified is True
        assert doc.status == KYCDocument.Status.VALIDATED

    def test_kyc_validation_task_rejection(self):
        user = User.objects.create_user(username='testuser', id_card_number=None)
        doc = KYCDocument.objects.create(user=user, document='test.jpg')

        validate_kyc_documents(doc.id)

        user.refresh_from_db()
        doc.refresh_from_db()

        assert user.is_kyc_verified is False
        assert doc.status == KYCDocument.Status.REJECTED
        assert "Missing ID card number" in doc.rejection_reason
