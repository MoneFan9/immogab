from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PaymentTransaction
from .providers.airtel import AirtelMoneyGateway
from .providers.moov import MoovMoneyGateway

from rest_framework.permissions import AllowAny

class MobileMoneyWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, provider):
        if provider == 'airtel':
            gateway = AirtelMoneyGateway()
        elif provider == 'moov':
            gateway = MoovMoneyGateway()
        else:
            return Response({"error": "Unknown provider"}, status=status.HTTP_400_BAD_REQUEST)

        result = gateway.handle_webhook(request.data, request.headers)

        if result["status"] == "success":
            try:
                tx = PaymentTransaction.objects.get(transaction_id=result["transaction_id"])
                tx.status = PaymentTransaction.PaymentStatus.SUCCESS
                tx.external_reference = result["external_reference"]
                tx.save()
                return Response({"status": "processed"}, status=status.HTTP_200_OK)
            except PaymentTransaction.DoesNotExist:
                return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "failed"}, status=status.HTTP_200_OK)
