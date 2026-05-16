from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from escrow.services import freeze_escrow
from escrow.tasks import schedule_escrow_release
from django.utils import timezone
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

        # If it's an event space, we freeze an escrow (caution)
        if booking.property.property_type == 'espace_evenementiel':
            # Logic refined: we freeze a caution of 100,000 XAF for events by default
            # or a percentage of the total price.
            caution_amount = Decimal('100000')
            escrow = freeze_escrow(booking, caution_amount)

            # Schedule the release task (eta = booking.end_time)
            schedule_escrow_release.apply_async((escrow.id,), eta=booking.end_time)
