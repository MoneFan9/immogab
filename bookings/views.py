from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from escrow.services import freeze_escrow
from escrow.tasks import schedule_escrow_release
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        # Calculate a mock total price if not provided (simplified for this task)
        # In a real app, logic would be more complex based on property rates
        duration = booking.end_time - booking.start_time
        hours = Decimal(duration.total_seconds() / 3600).quantize(Decimal('1.'), rounding='ROUND_UP')

        if booking.property.price_per_hour:
            booking.total_price = hours * booking.property.price_per_hour
            booking.save()

        # If it's an event space or has a configured caution, we freeze an escrow
        if booking.property.property_type == 'espace_evenementiel' or booking.property.caution_amount > 0:
            caution_amount = booking.property.caution_amount
            # Fallback for event spaces if not set
            if caution_amount == 0 and booking.property.property_type == 'espace_evenementiel':
                caution_amount = Decimal('100000')

            escrow = freeze_escrow(booking, caution_amount)

            # Schedule the release task after grace period (end_time + 2 hours)
            release_eta = booking.end_time + timedelta(hours=2)
            schedule_escrow_release.apply_async((escrow.id,), eta=release_eta)
