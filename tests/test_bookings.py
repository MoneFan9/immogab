import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import User
from properties.models import Property
from bookings.models import Booking
from bookings.services import check_booking_overlap

@pytest.mark.django_db
def test_booking_no_overlap():
    user = User.objects.create_user(username="testuser")
    prop = Property.objects.create(
        title="Test Property",
        property_type="ESPACE_EVENEMENTIEL",
        province="Estuaire"
    )

    # Booking 1: 10:00 to 12:00
    b1_start = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
    b1_end = b1_start + timedelta(hours=2)

    Booking.objects.create(
        user=user,
        property=prop,
        start_time=b1_start,
        end_time=b1_end,
        status='PAID'
    )

    # New Booking: 12:00 to 14:00 (Starts exactly when b1 ends)
    new_start = b1_end
    new_end = new_start + timedelta(hours=2)

    # Should not overlap
    assert check_booking_overlap(prop.id, new_start, new_end) is False

@pytest.mark.django_db
def test_booking_overlap_detected():
    user = User.objects.create_user(username="testuser2")
    prop = Property.objects.create(
        title="Test Property 2",
        property_type="ESPACE_EVENEMENTIEL",
        province="Estuaire"
    )

    # Booking 1: 10:00 to 12:00
    b1_start = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)
    b1_end = b1_start + timedelta(hours=2)

    Booking.objects.create(
        user=user,
        property=prop,
        start_time=b1_start,
        end_time=b1_end,
        status='PAID'
    )

    # New Booking: 11:30 to 13:00 (Starts during b1)
    new_start = b1_start + timedelta(hours=1.5)
    new_end = new_start + timedelta(hours=1.5)

    # Should overlap
    assert check_booking_overlap(prop.id, new_start, new_end) is True

@pytest.mark.django_db
def test_booking_overlap_inner():
    user = User.objects.create_user(username="testuser3")
    prop = Property.objects.create(
        title="Test Property 3",
        property_type="ESPACE_EVENEMENTIEL",
        province="Estuaire"
    )

    # Booking 1: 09:00 to 17:00
    b1_start = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
    b1_end = b1_start + timedelta(hours=8)

    Booking.objects.create(
        user=user,
        property=prop,
        start_time=b1_start,
        end_time=b1_end,
        status='PAID'
    )

    # New Booking: 12:00 to 13:00 (Inside b1)
    new_start = b1_start + timedelta(hours=3)
    new_end = new_start + timedelta(hours=1)

    assert check_booking_overlap(prop.id, new_start, new_end) is True
