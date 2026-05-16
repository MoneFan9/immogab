from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
import logging

logger = logging.getLogger(__name__)

class MobileMoneyWebhookView(APIView):
    """
    Endpoint for receiving asynchronous notifications from mobile money providers.
    In this mock version, it logs the callback and confirms reception.
    """
    permission_classes = [] # Ideally restricted by IP or secret header

    def post(self, request, provider, *args, **kwargs):
        data = request.data
        reference = data.get('reference')
        external_status = data.get('status') # e.g. 'SUCCESS' or 'FAILED'

        logger.info(f"Received webhook from {provider} for reference {reference}: {external_status}")

        try:
            payment = Payment.objects.get(reference=reference)
            # In a real scenario, we would verify signatures and update status here
            # But our Celery task already simulates the update for the mock.
            return Response({"status": "acknowledged"}, status=status.HTTP_200_OK)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
