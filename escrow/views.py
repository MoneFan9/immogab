from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Escrow
from .serializers import EscrowSerializer
from .services import claim_escrow

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
        if escrow.status != Escrow.EscrowStatus.FROZEN:
            return Response(
                {"error": f"La caution ne peut pas être réclamée car son statut est: {escrow.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        claim_escrow(escrow)
        return Response({"status": "Tapage nocturne signalé, la caution est bloquée (CLAIMED)."}, status=status.HTTP_200_OK)
