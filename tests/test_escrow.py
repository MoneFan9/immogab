import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import User
from properties.models import Property
from bookings.models import Booking
from payments.models import Escrow
from payments.services import freeze_escrow
from payments.tasks import release_escrow_after_event

@pytest.mark.django_db
def test_escrow_freeze_and_release():
    # Setup
    user = User.objects.create_user(username='testuser', password='password')
    prop = Property.objects.create(
        title='Event Space',
        property_type='ESPACE_EVENEMENTIEL',
        province='ESTUAIRE',
        city='Libreville',
        neighborhood='Sablière'
    )
    start_time = timezone.now() + timedelta(hours=1)
    end_time = timezone.now() + timedelta(hours=5)
    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=start_time,
        end_time=end_time
    )

    # 1. Test Freeze
    amount = 100000.00
    escrow = freeze_escrow(booking, amount)
    assert escrow.status == 'FROZEN'
    assert escrow.amount == amount
    assert booking.escrow == escrow

    # 2. Test Release (No noise)
    result = release_escrow_after_event(booking.id)
    assert "RELEASED successfully" in result
    escrow.refresh_from_db()
    assert escrow.status == 'RELEASED'
    assert escrow.released_at is not None

@pytest.mark.django_db
def test_escrow_forfeit_on_noise():
    # Setup
    user = User.objects.create_user(username='testuser2', password='password')
    prop = Property.objects.create(
        title='Event Space 2',
        property_type='ESPACE_EVENEMENTIEL',
        province='ESTUAIRE',
        city='Libreville',
        neighborhood='Sablière'
    )
    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(hours=2),
        has_noise_report=True # Noise reported!
    )
    freeze_escrow(booking, 100000)

    # Test Forfeit
    result = release_escrow_after_event(booking.id)
    assert "FORFEITED due to noise report" in result
    booking.escrow.refresh_from_db()
    assert booking.escrow.status == 'FORFEITED'
