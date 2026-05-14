from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Escrow
from .serializers import EscrowSerializer

class EscrowViewSet(viewsets.ModelViewSet):
    queryset = Escrow.objects.all()
    serializer_class = EscrowSerializer

    @action(detail=True, methods=['post'])
    def report_noise(self, request, pk=None):
        escrow = self.get_object()
        escrow.has_noise_complaint = True
        escrow.save()
        return Response({'status': 'noise complaint reported'})
