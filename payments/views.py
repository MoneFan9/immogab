import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentTransaction
from .logic import calculate_revenue_split
from django.conf import settings
from decimal import Decimal

class MobileMoneyWebhookView(APIView):
    permission_classes = []  # Public endpoint for provider webhooks

    def post(self, request, provider):
        # BASIC SECURITY: Check for a shared secret in headers if not in DEBUG
        # In a real Gabon scenario, we would validate IP or signature.
        if not settings.DEBUG:
            webhook_key = request.headers.get('X-ImmoGab-Webhook-Key')
            if webhook_key != os.getenv('WEBHOOK_SECRET_KEY'):
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        if provider == 'airtel':
            # Simplified Airtel logic: airtel_status '00' is success
            tx_id = data.get('custom_id')
            external_ref = data.get('airtel_ref')
            success = data.get('airtel_status') == '00'
        elif provider == 'moov':
            # Simplified Moov logic: result 'completed' is success
            tx_id = data.get('client_reference')
            external_ref = data.get('moov_trans_id')
            success = data.get('result') == 'completed'
        else:
            return Response({"error": "Unknown provider"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tx = PaymentTransaction.objects.get(transaction_id=tx_id)
            tx.external_reference = external_ref

            if success:
                tx.status = 'SUCCESS'
                # Apply revenue split logic
                commission_rate = getattr(settings, 'IMMOGAB_COMMISSION_RATE', Decimal('0.15'))
                split = calculate_revenue_split(tx.amount, commission_rate)
                tx.commission_amount = split['commission']
                tx.host_amount = split['host']
            else:
                tx.status = 'FAILED'

            tx.save()

            if tx.status == 'SUCCESS' and tx.booking:
                tx.booking.status = 'PAID'
                tx.booking.save()

            return Response({"status": "received"}, status=status.HTTP_200_OK)
        except PaymentTransaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
