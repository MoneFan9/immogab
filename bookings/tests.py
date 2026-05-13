import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from core.models import User
from properties.models import Property
from bookings.models import Booking
from decimal import Decimal

@pytest.mark.django_db
class TestBookingModel:
    def setup_method(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.property = Property.objects.create(
            title="Test Villa",
            description="A test villa",
            property_type="villa",
            price=Decimal("5000.00"),
            address="123 Test St",
            city="Libreville",
            province="estuaire",
            owner=self.user
        )

    def test_calculate_total_price_exact_hour(self):
        start = timezone.now()
        end = start + timedelta(hours=2)
        booking = Booking(
            property=self.property,
            user=self.user,
            start_time=start,
            end_time=end
        )
        # Price is 5000 * 2 = 10000
        assert booking.calculate_total_price() == Decimal("10000.00")

    def test_calculate_total_price_rounded_up(self):
        start = timezone.now()
        end = start + timedelta(hours=1, minutes=1)
        booking = Booking(
            property=self.property,
            user=self.user,
            start_time=start,
            end_time=end
        )
        # 1h01m should be rounded to 2h: 5000 * 2 = 10000
        assert booking.calculate_total_price() == Decimal("10000.00")

    def test_booking_save_calculates_price(self):
        start = timezone.now()
        end = start + timedelta(hours=3)
        booking = Booking.objects.create(
            property=self.property,
            user=self.user,
            start_time=start,
            end_time=end
        )
        assert booking.total_price == Decimal("15000.00")

    def test_booking_overlap_prevention(self):
        start1 = timezone.now()
        end1 = start1 + timedelta(hours=2)
        Booking.objects.create(
            property=self.property,
            user=self.user,
            start_time=start1,
            end_time=end1
        )

        # Overlapping booking
        start2 = start1 + timedelta(hours=1)
        end2 = start1 + timedelta(hours=3)
        overlapping_booking = Booking(
            property=self.property,
            user=self.user,
            start_time=start2,
            end_time=end2
        )

        with pytest.raises(ValidationError, match="Cette propriété est déjà réservée"):
            overlapping_booking.full_clean()

    def test_start_before_end_validation(self):
        start = timezone.now()
        end = start - timedelta(hours=1)
        booking = Booking(
            property=self.property,
            user=self.user,
            start_time=start,
            end_time=end
        )
        with pytest.raises(ValidationError, match="La date de début doit être antérieure"):
            booking.full_clean()
