import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import User
from properties.models import Property
from bookings.models import Booking
from immogab.services import check_booking_overlap

@pytest.fixture
def property(db):
    return Property.objects.create(
        title="Villa à Libreville",
        description="Belle villa",
        property_type="villa",
        province="estuaire",
        location="Libreville",
        price_per_hour=5000
    )

@pytest.mark.django_db
def test_booking_no_overlap(property):
    # Booking 1: 10:00 to 12:00
    b1_start = timezone.now() + timedelta(hours=10)
    b1_end = b1_start + timedelta(hours=2)

    # We need a user to create a booking
    user = User.objects.create_user(username="testuser", password="password")

    Booking.objects.create(
        user=user,
        property=property,
        start_time=b1_start,
        end_time=b1_end,
        status='PAID'
    )

    # New Booking: 12:00 to 14:00 (Starts exactly when b1 ends)
    new_start = b1_end
    new_end = new_start + timedelta(hours=2)

    # Should not overlap
    assert check_booking_overlap(new_start, new_end, property.id) is False

@pytest.mark.django_db
def test_booking_overlap_detected(property):
    # Booking 1: 10:00 to 12:00
    b1_start = timezone.now() + timedelta(hours=10)
    b1_end = b1_start + timedelta(hours=2)

    user = User.objects.create_user(username="testuser2", password="password")

    Booking.objects.create(
        user=user,
        property=property,
        start_time=b1_start,
        end_time=b1_end,
        status='PAID'
    )

    # New Booking: 11:30 to 13:00 (Starts during b1)
    new_start = b1_start + timedelta(hours=1, minutes=30)
    new_end = new_start + timedelta(hours=1, minutes=30)

    # Should overlap
    assert check_booking_overlap(new_start, new_end, property.id) is True
