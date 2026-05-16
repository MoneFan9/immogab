import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from payments.providers.airtel import AirtelMoneyGateway
from payments.providers.moov import MoovMoneyGateway
from payments.models import PaymentTransaction

@csrf_exempt
@require_POST
def payment_webhook(request, provider):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if provider == "airtel":
        gateway = AirtelMoneyGateway()
    elif provider == "moov":
        gateway = MoovMoneyGateway()
    else:
        return JsonResponse({"error": "Unknown provider"}, status=404)

    # Process webhook using the provider gateway
    result = gateway.handle_webhook(data, request.headers)

    if result.get("transaction_id"):
        try:
            tx = PaymentTransaction.objects.get(transaction_id=result["transaction_id"])
            tx.status = 'SUCCESS' if result["status"] == "success" else 'FAILED'
            tx.external_reference = result.get("external_reference")
            tx.save()
        except PaymentTransaction.DoesNotExist:
            # Optionally log orphan webhooks
            pass

    return JsonResponse({"status": "received"})
