from celery import shared_task
from .models import User
import time

@shared_task
def validate_kyc_task(user_id):
    """
    Simulates asynchronous KYC document validation.
    In a real scenario, this might involve OCR or external API calls.
    """
    try:
        user = User.objects.get(id=user_id)

        # Simulate processing time
        time.sleep(2)

        # Simple validation logic: if CNI number is provided, mark as verified
        if user.cni_number:
            user.is_kyc_verified = True
            user.save()
            return f"KYC verified for user {user_id}"
        else:
            return f"KYC validation failed for user {user_id}: CNI missing"

    except User.DoesNotExist:
        return f"User {user_id} not found"
