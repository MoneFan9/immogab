from django.db import transaction
from django.utils import timezone
from .models import Booking
from escrow.models import Escrow
from decimal import Decimal

def process_booking_payment(booking_id):
    """
    Service to process payment for a booking.
    Updates status to PAID and handles escrow for event spaces.
    """
    with transaction.atomic():
        booking = Booking.objects.select_for_update().get(id=booking_id)

        if booking.status == 'PAID':
            return booking

        booking.status = 'PAID'
        booking.save()

        # If it's an event space, freeze the escrow (caution)
        if booking.property.property_type == 'espace_evenementiel':
            # Calculate caution amount (e.g., 50% of total price or fixed amount)
            # Directive says up to 1,000,000 FCFA for noise complaints, but escrow is usually a deposit.
            # Let's assume a standard caution of 50,000 FCFA for event spaces if not specified.
            caution_amount = Decimal('50000.00')

            Escrow.objects.create(
                booking=booking,
                amount=caution_amount,
                is_frozen=True
            )

            # Schedule release task (24h after end_time)
            from escrow.tasks import release_escrow_task
            eta = booking.end_time + timezone.timedelta(hours=24)
            from django.conf import settings
            if getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
                # When eager, eta might still try to use a broker if not careful in some celery versions
                # but usually it just runs immediately.
                # However, apply_async with eta in eager mode sometimes still fails if no broker.
                release_escrow_task.delay(booking.escrow.id)
            else:
                release_escrow_task.apply_async((booking.escrow.id,), eta=eta)

    return booking
