from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import PaymentTransaction
from .tasks import simulate_mobile_money_webhook

class MobileMoneyWebhookView(APIView):
    """
    Webhook endpoint for mobile money providers (Airtel/Moov).
    Validates security header before processing payment updates.
    """
    permission_classes = [AllowAny]

    def post(self, request, provider):
        # Security validation
        webhook_key = request.headers.get('X-ImmoGab-Webhook-Key')
        if not settings.DEBUG and webhook_key != settings.WEBHOOK_SECRET:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        # Handle different provider payload formats
        if provider == 'airtel':
            transaction_id = request.data.get('custom_id')
            external_ref = request.data.get('airtel_ref')
            raw_status = 'SUCCESS' if request.data.get('airtel_status') == '00' else 'FAILED'
        elif provider == 'moov':
            transaction_id = request.data.get('client_reference')
            external_ref = request.data.get('moov_trans_id')
            raw_status = 'SUCCESS' if request.data.get('result') == 'completed' else 'FAILED'
        else:
            transaction_id = request.data.get('transaction_id')
            external_ref = request.data.get('external_ref')
            raw_status = request.data.get('status')

        if not transaction_id:
            return Response({"error": "Missing transaction_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = PaymentTransaction.objects.get(transaction_id=transaction_id)
            payment.external_reference = external_ref

            if raw_status == 'SUCCESS':
                # Trigger internal processing (async)
                simulate_mobile_money_webhook.delay(payment.id)
            else:
                payment.status = PaymentTransaction.PaymentStatus.FAILED
                payment.save()

            return Response({"message": "Webhook received"}, status=status.HTTP_200_OK)
        except PaymentTransaction.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
