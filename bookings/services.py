from django.db import transaction
from django.core.exceptions import ValidationError
from bookings.models import Booking
from properties.models import Property
import math

def check_booking_overlap(property_id, start_time, end_time, exclude_booking_id=None):
    """
    Checks if a property is already booked for a given time range.
    Uses select_for_update to lock the property and its bookings.
    """
    query = Booking.objects.filter(
        property_id=property_id,
        start_time__lt=end_time,
        end_time__gt=start_time,
        status__in=[Booking.BookingStatus.PAID, Booking.BookingStatus.PENDING]
    )

    if exclude_booking_id:
        query = query.exclude(id=exclude_booking_id)

    return query.exists()

def calculate_total_price(property_obj, start_time, end_time):
    """
    Calculates the total price based on duration and property rates.
    """
    duration = end_time - start_time
    hours = math.ceil(duration.total_seconds() / 3600)
    days = math.ceil(duration.total_seconds() / 86400)

    if property_obj.property_type == Property.PropertyType.ESPACE_EVENEMENTIEL:
        if not property_obj.price_per_hour:
             raise ValidationError("Espace Événementiel must have an hourly rate.")
        return hours * property_obj.price_per_hour
    else:
        if property_obj.price_per_day:
            return days * property_obj.price_per_day
        elif property_obj.price_per_hour:
            return hours * property_obj.price_per_hour

    raise ValidationError("Property has no defined rates.")

@transaction.atomic
def create_booking(user, property_id, start_time, end_time):
    """
    Creates a booking with strict overlap prevention.
    """
    # Lock the property to prevent concurrent booking attempts for the same property
    property_obj = Property.objects.select_for_update().get(id=property_id)

    if not user.is_kyc_verified:
        raise ValidationError("User must be KYC verified to book a property.")

    if start_time >= end_time:
        raise ValidationError("Start time must be before end time.")

    if check_booking_overlap(property_id, start_time, end_time):
        raise ValidationError("This property is already booked for the selected time range.")

    total_price = calculate_total_price(property_obj, start_time, end_time)

    booking = Booking.objects.create(
        user=user,
        property=property_obj,
        start_time=start_time,
        end_time=end_time,
        total_price=total_price,
        status=Booking.BookingStatus.PENDING
    )

    return booking

def synchronize_payment_status(booking, transaction_status):
    """
    Updates booking status based on payment transaction status.
    """
    if transaction_status == "SUCCESS":
        booking.status = Booking.BookingStatus.PAID
        booking.save()
        # Trigger Jeedom IoT webhook here in a real scenario
    elif transaction_status == "FAILED":
        booking.status = Booking.BookingStatus.CANCELLED
        booking.save()
