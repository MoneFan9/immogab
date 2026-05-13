from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from .services import process_booking_payment

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and creating bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users can only see their own bookings unless they are staff
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current authenticated user
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """
        Trigger payment processing for a specific booking.
        """
        booking = self.get_object()
        updated_booking = process_booking_payment(booking.id)

        if updated_booking:
            serializer = self.get_serializer(updated_booking)
            return Response(serializer.data)
        return Response(
            {"error": "Impossible de traiter le paiement."},
            status=status.HTTP_400_BAD_REQUEST
        )
