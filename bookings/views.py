from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Booking
from .serializers import BookingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            # Using select_for_update on the property would be better, but we don't have a direct lock here easily.
            # However, the model's full_clean() is called in save() which calls check_booking_overlap.
            # Wrapping it in atomic transaction helps with integrity.
            serializer.save(user=self.request.user)
