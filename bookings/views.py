from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from properties.models import Property
from bookings.models import Booking
from bookings.serializers import PropertySerializer, BookingSerializer
from bookings.services import create_booking
from django.core.exceptions import ValidationError

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            booking = create_booking(
                user=self.request.user,
                property_id=serializer.validated_data.get("property").id,
                start_time=serializer.validated_data.get("start_time"),
                end_time=serializer.validated_data.get("end_time")
            )
            serializer.instance = booking
        except ValidationError as e:
            raise ValidationError(e.message)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
