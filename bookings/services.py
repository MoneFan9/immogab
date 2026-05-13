from django.db.models import Q
from .models import Booking

def check_booking_overlap(property_id, new_start, new_end, exclude_booking_id=None):
    """
    Checks if a new booking interval overlaps with any existing ACTIVE bookings for a property.
    Active bookings are those not 'CANCELLED' or 'FAILED'.
    """
    query = Booking.objects.filter(
        property_id=property_id,
        start_time__lt=new_end,
        end_time__gt=new_start
    ).exclude(status__in=['CANCELLED', 'FAILED'])

    if exclude_booking_id:
        query = query.exclude(id=exclude_booking_id)

    return query.exists()

def update_booking_status(booking_id, payment_status):
    """
    Synchronizes booking status with payment status.
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        if payment_status == 'SUCCESS':
            booking.status = 'PAID'
        elif payment_status == 'FAILURE':
            booking.status = 'FAILED'
        booking.save()
        return True
    except Booking.DoesNotExist:
        return False
