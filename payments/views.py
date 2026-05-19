from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging

from .models import PaymentTransaction
from .factory import get_payment_gateway
from bookings.services import synchronize_payment_status

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class MobileMoneyWebhookView(View):
    """
    Generic webhook view for Mobile Money providers (Airtel, Moov).
    """
    def post(self, request, provider):
        try:
            data = json.loads(request.body)
            headers = request.headers

            # 1. Get appropriate gateway
            gateway = get_payment_gateway(provider)

            # 2. Parse provider-specific data
            result = gateway.handle_webhook(data, headers)

            transaction_id = result.get('transaction_id')
            status = result.get('status')
            external_ref = result.get('external_reference')

            if not transaction_id:
                return JsonResponse({"error": "Missing transaction_id in webhook data"}, status=400)

            # 3. Update PaymentTransaction
            try:
                tx = PaymentTransaction.objects.get(transaction_id=transaction_id)
                tx.status = status
                tx.external_reference = external_ref
                tx.save()

                # 4. Synchronize with Booking
                if tx.booking:
                    synchronize_payment_status(tx.booking, status)

                return JsonResponse({"status": "received", "transaction_id": transaction_id})

            except PaymentTransaction.DoesNotExist:
                logger.error(f"Transaction {transaction_id} not found for provider {provider}")
                return JsonResponse({"error": "Transaction not found"}, status=404)

        except (ValueError, json.JSONDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.exception("Error processing webhook")
            return JsonResponse({"error": "Internal server error"}, status=500)
