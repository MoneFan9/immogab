import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from core.models import User
from properties.models import Property
from bookings.models import Booking
from bookings.services import process_booking_payment
from escrow.models import Escrow
from escrow.tasks import release_escrow_task
from decimal import Decimal

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def event_property(db):
    return Property.objects.create(
        title="Salle de Fête",
        description="Grande salle",
        property_type="espace_evenementiel",
        province="estuaire",
        location="Libreville",
        price_per_hour=Decimal("10000.00")
    )

@pytest.fixture
def normal_property(db):
    return Property.objects.create(
        title="Appartement",
        description="Petit appartement",
        property_type="appartement",
        province="estuaire",
        location="Libreville",
        price_per_hour=Decimal("5000.00")
    )

from unittest.mock import patch

@pytest.mark.django_db
def test_escrow_frozen_for_event_space(user, event_property):
    # Create a booking
    start_time = timezone.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=4)
    booking = Booking.objects.create(
        user=user,
        property=event_property,
        start_time=start_time,
        end_time=end_time
    )

    assert booking.status == "PENDING"

    # Process payment, but patch the task to prevent eager execution from releasing it immediately
    with patch("escrow.tasks.release_escrow_task.apply_async") as mock_apply, \
         patch("escrow.tasks.release_escrow_task.delay") as mock_delay:
        updated_booking = process_booking_payment(booking.id)

    assert updated_booking.status == "PAID"
    # Check if escrow was created and frozen
    escrow = Escrow.objects.get(booking=updated_booking)
    assert escrow.is_frozen is True
    assert escrow.is_released is False
    assert escrow.amount == Decimal("50000.00")
    assert mock_delay.called or mock_apply.called

@pytest.mark.django_db
def test_no_escrow_for_normal_property(user, normal_property):
    start_time = timezone.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=4)
    booking = Booking.objects.create(
        user=user,
        property=normal_property,
        start_time=start_time,
        end_time=end_time
    )

    process_booking_payment(booking.id)

    # Escrow should not exist
    assert not Escrow.objects.filter(booking=booking).exists()

@pytest.mark.django_db
def test_escrow_release_task_success(user, event_property):
    start_time = timezone.now() - timedelta(days=2)
    end_time = start_time + timedelta(hours=4)
    booking = Booking.objects.create(
        user=user,
        property=event_property,
        start_time=start_time,
        end_time=end_time
    )

    # Prevent eager task execution during payment
    with patch("escrow.tasks.release_escrow_task.delay"):
        process_booking_payment(booking.id)

    escrow = Escrow.objects.get(booking=booking)

    # Run task manually
    result = release_escrow_task(escrow.id)

    escrow.refresh_from_db()
    assert escrow.is_released is True
    assert escrow.is_frozen is False
    assert "successfully released" in result

@pytest.mark.django_db
def test_escrow_no_release_on_noise_complaint(user, event_property):
    start_time = timezone.now() - timedelta(days=2)
    end_time = start_time + timedelta(hours=4)
    booking = Booking.objects.create(
        user=user,
        property=event_property,
        start_time=start_time,
        end_time=end_time
    )

    # Prevent eager task execution during payment
    with patch("escrow.tasks.release_escrow_task.delay"):
        process_booking_payment(booking.id)

    escrow = Escrow.objects.get(booking=booking)
    escrow.has_noise_complaint = True
    escrow.save()

    # Run task manually
    result = release_escrow_task(escrow.id)

    escrow.refresh_from_db()
    assert escrow.is_released is False
    assert escrow.is_frozen is True
    assert "remains frozen" in result
