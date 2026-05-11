import pytest
from django.utils import timezone
from datetime import timedelta
from core.models import User
from properties.models import Property
from bookings.models import Booking
from bookings.services import check_booking_overlap, update_booking_status

@pytest.fixture
def test_data(db):
    user = User.objects.create_user(username="jules")
    prop = Property.objects.create(
        title="Salle de Fête",
        property_type="ESPACE_EVENEMENTIEL",
        province="Estuaire"
    )
    return user, prop

@pytest.mark.django_db
def test_double_booking_prevention_same_property(test_data):
    user, prop = test_data
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=5)

    # Create first booking
    Booking.objects.create(user=user, property=prop, start_time=start, end_time=end, status='PAID')

    # Try to book same property at same time
    assert check_booking_overlap(prop.id, start, end) is True

@pytest.mark.django_db
def test_booking_overlap_ignores_cancelled(test_data):
    user, prop = test_data
    start = timezone.now() + timedelta(days=1)
    end = start + timedelta(hours=5)

    # Create cancelled booking
    Booking.objects.create(user=user, property=prop, start_time=start, end_time=end, status='CANCELLED')

    # New booking at same time should be allowed
    assert check_booking_overlap(prop.id, start, end) is False

@pytest.mark.django_db
def test_update_booking_status_success(test_data):
    user, prop = test_data
    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        status='PENDING'
    )

    success = update_booking_status(booking.id, 'SUCCESS')
    booking.refresh_from_db()

    assert success is True
    assert booking.status == 'PAID'

@pytest.mark.django_db
def test_update_booking_status_failure(test_data):
    user, prop = test_data
    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=1),
        status='PENDING'
    )

    success = update_booking_status(booking.id, 'FAILURE')
    booking.refresh_from_db()

    assert success is True
    assert booking.status == 'FAILED'

@pytest.mark.django_db
def test_booking_clean_raises_validation_error_on_overlap(test_data):
    from django.core.exceptions import ValidationError
    user, prop = test_data
    start = timezone.now() + timedelta(days=2)
    end = start + timedelta(hours=5)

    # Create first booking
    Booking.objects.create(user=user, property=prop, start_time=start, end_time=end, status='PAID')

    # Try to create another one that overlaps
    overlapping_booking = Booking(user=user, property=prop, start_time=start + timedelta(hours=1), end_time=end + timedelta(hours=1))

    with pytest.raises(ValidationError, match="Cette propriété est déjà réservée pour ce créneau horaire."):
        overlapping_booking.clean()
