from celery import shared_task
from django.contrib.auth import get_user_model
import time

User = get_user_model()

@shared_task
def validate_kyc_document_async(user_id):
    try:
        user = User.objects.get(id=user_id)
        # Simulating document validation (OCR, etc.)
        time.sleep(2)  # Artificial delay

        if user.kyc_document and user.cni_number:
            user.is_kyc_verified = True
            user.save()
            return f"KYC verified for user {user.username}"
        else:
            return f"KYC validation failed for user {user.username}: Missing document or CNI number"
    except User.DoesNotExist:
        return f"User with id {user_id} does not exist"
