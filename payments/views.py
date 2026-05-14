import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .gateways.mock import MockPaymentGateway

@csrf_exempt
@require_POST
def mock_payment_webhook(request):
    """
    Endpoint that receives payment notifications.
    """
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    gateway = MockPaymentGateway()
    result = gateway.handle_webhook(payload)

    # Here you would typically update the Booking status in the database
    # For now, we just return the result of the gateway processing.

    return JsonResponse(result)
