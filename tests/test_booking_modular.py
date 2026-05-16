import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import User
from properties.models import Property
from bookings.models import Booking
from bookings.services import create_booking, check_booking_overlap
from django.core.exceptions import ValidationError
from django.db import transaction

@pytest.mark.django_db
class TestBookingService:
    @pytest.fixture
    def verified_user(self):
        return User.objects.create_user(
            username="verified",
            is_kyc_verified=True,
            id_card_number="123"
        )

    @pytest.fixture
    def unverified_user(self):
        return User.objects.create_user(
            username="unverified",
            is_kyc_verified=False
        )

    @pytest.fixture
    def event_space(self):
        return Property.objects.create(
            title="Espace Gabao",
            property_type=Property.PropertyType.ESPACE_EVENEMENTIEL,
            price_per_hour=10000,
            province=Property.Province.ESTUAIRE,
            city="Libreville",
            neighborhood="Angondjé"
        )

    def test_create_booking_success(self, verified_user, event_space):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=4)

        booking = create_booking(verified_user, event_space.id, start, end)

        assert booking.id is not None
        assert booking.total_price == 40000
        assert booking.status == Booking.BookingStatus.PENDING

    def test_create_booking_unverified_fails(self, unverified_user, event_space):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=4)

        with pytest.raises(ValidationError, match="User must be KYC verified"):
            create_booking(unverified_user, event_space.id, start, end)

    def test_double_booking_prevention(self, verified_user, event_space):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=4)

        # First booking
        create_booking(verified_user, event_space.id, start, end)

        # Second booking overlapping
        overlap_start = start + timedelta(hours=2)
        overlap_end = overlap_start + timedelta(hours=2)

        with pytest.raises(ValidationError, match="already booked"):
            create_booking(verified_user, event_space.id, overlap_start, overlap_end)

    def test_booking_synchronization_with_payment(self, verified_user, event_space):
        from payments.gateways import MockPaymentGateway

        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=4)
        booking = create_booking(verified_user, event_space.id, start, end)

        gateway = MockPaymentGateway()
        gateway.process_payment(booking, booking.total_price)

        booking.refresh_from_db()
        assert booking.status == Booking.BookingStatus.PAID
