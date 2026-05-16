import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import User
from properties.models import Property
from bookings.models import Booking
from escrow.models import Escrow
from decimal import Decimal

@pytest.mark.django_db
def test_booking_hourly_pricing():
    # Setup
    user = User.objects.create(username="testuser")
    prop = Property.objects.create(
        title="Test Villa",
        price_per_hour=Decimal("1000.00"),
        province="ESTUAIRE",
        city="Libreville",
        neighborhood="Angondje"
    )

    # 2 hours booking
    start = timezone.now()
    end = start + timedelta(hours=2)

    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=start,
        end_time=end
    )

    assert booking.total_price == Decimal("2000.00")

@pytest.mark.django_db
def test_booking_partial_hour_pricing():
    # Setup
    user = User.objects.create(username="testuser2")
    prop = Property.objects.create(
        title="Test Villa 2",
        price_per_hour=Decimal("1000.00"),
        province="ESTUAIRE",
        city="Libreville",
        neighborhood="Angondje"
    )

    # 1 hour and 15 minutes -> counts as 2 hours
    start = timezone.now()
    end = start + timedelta(hours=1, minutes=15)

    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=start,
        end_time=end
    )

    assert booking.total_price == Decimal("2000.00")

@pytest.mark.django_db
def test_escrow_anti_noise_logic():
    # Setup
    user = User.objects.create(username="testuser3")
    prop = Property.objects.create(
        title="Test Villa 3",
        price_per_hour=Decimal("1000.00"),
        province="ESTUAIRE",
        city="Libreville",
        neighborhood="Angondje"
    )

    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1)
    )

    escrow = Escrow.objects.create(
        booking=booking,
        amount=Decimal("50000.00")
    )

    # Initial state
    assert escrow.is_frozen is True
    assert escrow.is_released is False
    assert escrow.can_be_released() is True

    # With noise complaint
    escrow.has_noise_complaint = True
    escrow.save()

    assert escrow.can_be_released() is False
    assert escrow.release() is False
    assert escrow.is_released is False

    # Clear noise complaint
    escrow.has_noise_complaint = False
    escrow.save()

    assert escrow.can_be_released() is True
    assert escrow.release() is True
    assert escrow.is_released is True
    assert escrow.is_frozen is False
