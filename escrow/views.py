from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Escrow
from .serializers import EscrowSerializer
from .services import report_noise_complaint

class EscrowViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Escrow.objects.all()
    serializer_class = EscrowSerializer

    @action(detail=True, methods=['post'], url_path='report-noise')
    def report_noise(self, request, pk=None):
        """
        Endpoint to report noise complaints for an active escrow.
        Usually called by an IoT device (Jeedom) or an admin.
        """
        escrow = self.get_object()
        if not escrow.is_frozen or escrow.is_released:
            return Response(
                {"error": "La caution n'est pas active ou est déjà libérée."},
                status=status.HTTP_400_BAD_REQUEST
            )

        report_noise_complaint(escrow)
        return Response({"status": "Tapage nocturne signalé, la caution est bloquée."}, status=status.HTTP_200_OK)
