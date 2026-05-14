from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .gateways.factory import PaymentFactory

class WebhookView(APIView):
    permission_classes = []  # Webhooks are usually called by external providers

    def post(self, request, provider):
        try:
            gateway = PaymentFactory.get_gateway(provider)
            result = gateway.handle_webhook(request.data, request.headers)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
