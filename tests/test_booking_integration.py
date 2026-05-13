import pytest
from django.utils import timezone
from datetime import timedelta
from core.models import User
from properties.models import Property
from bookings.models import Booking
from bookings.services import process_booking_payment

@pytest.mark.django_db
def test_booking_logic():
    # 1. Setup
    owner = User.objects.create_user(username="owner", password="password")
    customer = User.objects.create_user(username="customer", password="password")

    prop = Property.objects.create(
        title="Espace Event",
        property_type="espace_evenementiel",
        price_per_hour=10000,
        province="estuaire",
        owner=owner
    )

    start_time = timezone.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    # 2. Test booking creation and price calculation
    booking = Booking.objects.create(
        property=prop,
        user=customer,
        start_time=start_time,
        end_time=end_time
    )
    assert booking.total_price == 20000
    assert booking.status == 'PENDING'

    # 3. Test overlap prevention
    with pytest.raises(Exception): # ValidationError
        Booking.objects.create(
            property=prop,
            user=owner,
            start_time=start_time + timedelta(hours=1),
            end_time=start_time + timedelta(hours=3)
        )

    # 4. Test payment synchronization
    updated_booking = process_booking_payment(booking.id)
    assert updated_booking.status == 'PAID'
