import pytest
from django.utils import timezone
from datetime import timedelta
from core.models import User
from properties.models import Property
from bookings.models import Booking
from escrow.models import Escrow
from escrow.services import freeze_escrow, release_escrow, report_noise_complaint
from escrow.tasks import schedule_escrow_release
from unittest.mock import patch

@pytest.mark.django_db
class TestEscrowLogic:
    def setup_method(self):
        self.user = User.objects.create_user(username="testuser", password="password", id_card_number="GAB-TEST")
        self.property = Property.objects.create(
            title="Espace Event",
            property_type="espace_evenementiel",
            province="estuaire",
            price_per_hour=10000
        )
        self.booking = Booking.objects.create(
            user=self.user,
            property=self.property,
            start_time=timezone.now() - timedelta(hours=2),
            end_time=timezone.now() - timedelta(hours=1),
            status="CONFIRMED"
        )

    def test_freeze_escrow(self):
        escrow = freeze_escrow(self.booking, 100000)
        assert escrow.is_frozen is True
        assert escrow.amount == 100000
        assert escrow.frozen_at is not None

    def test_release_escrow_success(self):
        escrow = freeze_escrow(self.booking, 100000)
        success = release_escrow(escrow)
        assert success is True
        assert escrow.is_released is True
        assert escrow.released_at is not None

    def test_release_escrow_blocked_by_noise(self):
        escrow = freeze_escrow(self.booking, 100000)
        report_noise_complaint(escrow)
        success = release_escrow(escrow)
        assert success is False
        assert escrow.is_released is False
        assert escrow.has_noise_complaint is True

    def test_task_release_escrow_success(self):
        escrow = freeze_escrow(self.booking, 100000)
        # Booking ended 1 hour ago (in setup)
        result = schedule_escrow_release(escrow.id)
        assert result == "Released"
        escrow.refresh_from_db()
        assert escrow.is_released is True

    def test_task_release_escrow_too_early(self):
        future_booking = Booking.objects.create(
            user=self.user,
            property=self.property,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=2),
            status="CONFIRMED"
        )
        escrow = freeze_escrow(future_booking, 100000)
        result = schedule_escrow_release(escrow.id)
        assert result == "Too early"
        escrow.refresh_from_db()
        assert escrow.is_released is False
