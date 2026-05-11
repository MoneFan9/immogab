import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.tasks import validate_kyc_document_async
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
@patch('core.tasks.validate_kyc_document_async.delay')
def test_kyc_submission_triggers_task(mock_task, api_client):
    user = User.objects.create_user(username='testuser', password='password123')
    api_client.force_authenticate(user=user)

    url = reverse('kyc-submit')
    dummy_file = SimpleUploadedFile("test_cni.pdf", b"file_content", content_type="application/pdf")

    response = api_client.patch(url, {
        'cni_number': 'GAB12345',
        'kyc_document': dummy_file
    }, format='multipart', secure=True)

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.cni_number == 'GAB12345'
    assert user.kyc_document.name.startswith('kyc_documents/test_cni')
    mock_task.assert_called_once_with(user.id)

@pytest.mark.django_db
def test_kyc_async_task_success():
    dummy_file = SimpleUploadedFile("test_cni.pdf", b"file_content", content_type="application/pdf")
    user = User.objects.create_user(
        username='testuser',
        cni_number='GAB12345',
        kyc_document=dummy_file
    )

    with patch('time.sleep', return_value=None):
        result = validate_kyc_document_async(user.id)

    user.refresh_from_db()
    assert user.is_kyc_verified is True
    assert "verified" in result

@pytest.mark.django_db
def test_kyc_async_task_failure_missing_info():
    user = User.objects.create_user(username='testuser')

    with patch('time.sleep', return_value=None):
        result = validate_kyc_document_async(user.id)

    user.refresh_from_db()
    assert user.is_kyc_verified is False
    assert "failed" in result
