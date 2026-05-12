from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from properties.models import Property
from payments.services import freeze_escrow
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'status', 'has_noise_report')

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'property__property_type', 'property__province']

    def perform_create(self, serializer):
        with transaction.atomic():
            booking = serializer.save(user=self.request.user)

            # If it's an event booking and a caution amount is set, freeze the escrow
            if booking.property.property_type == 'ESPACE_EVENEMENTIEL' and booking.property.caution_amount > 0:
                freeze_escrow(booking, booking.property.caution_amount)

                # Schedule the release task with a 24-hour grace period after the event
                from payments.tasks import release_escrow_after_event
                GRACE_PERIOD = timedelta(hours=24)
                release_time = booking.end_time + GRACE_PERIOD
                release_escrow_after_event.apply_async((booking.id,), eta=release_time)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
