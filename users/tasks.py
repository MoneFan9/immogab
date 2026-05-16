from celery import shared_task
from django.utils import timezone
from .models import KYCDocument, User

@shared_task
def validate_kyc_documents(document_id):
    """
    Simulates an asynchronous KYC document validation process.
    In a real-world scenario, this might involve calling an external
    OCR service or a manual review API.
    """
    try:
        document = KYCDocument.objects.get(id=document_id)

        # Simulate processing delay
        # import time
        # time.sleep(5)

        # Simple heuristic for mock validation:
        # If the user has an ID card number, we validate.
        if document.user.id_card_number:
            document.status = KYCDocument.Status.VALIDATED
            document.user.is_kyc_verified = True
            document.user.save()
        else:
            document.status = KYCDocument.Status.REJECTED
            document.rejection_reason = "Missing ID card number on profile."

        document.reviewed_at = timezone.now()
        document.save()

        return f"Document {document_id} processed: {document.status}"

    except KYCDocument.DoesNotExist:
        return f"Document {document_id} not found"
