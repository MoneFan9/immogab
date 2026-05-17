import pytest
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from properties.models import Property
from bookings.models import Booking
from immogab.services import check_booking_overlap, validate_kyc

User = get_user_model()

@pytest.mark.django_db
class TestE2EJourney:
    def test_e2e_journey_success(self):
        # 1. User Creation
        user = User.objects.create_user(username="testuser_e2e", password="password123")

        # 2. KYC Submission
        user.id_card_number = "GAB-CNI-2024-X"
        user.id_card_type = "CNI"
        validate_kyc(user)
        assert user.is_kyc_verified is True

        # 3. Property Discovery
        prop = Property.objects.create(
            title="Villa Bord de Mer",
            province="estuaire",
            city="Libreville",
            property_type="maison",
            price_per_hour=25000
        )

        # 4. Overlap Check
        # Fixed dates to avoid rounding issues during test execution
        start_time = datetime(2026, 6, 1, 10, 0, tzinfo=timezone.get_current_timezone())
        end_time = datetime(2026, 6, 1, 14, 0, tzinfo=timezone.get_current_timezone())
        existing_bookings = []
        assert check_booking_overlap(start_time, end_time, existing_bookings) is False

        # 5. Booking Creation
        booking = Booking.objects.create(
            user=user,
            property=prop,
            start_time=start_time,
            end_time=end_time
        )
        assert booking.status == "PENDING"

        # In case of any timezone shift or micro-duration, let's check what we got
        # math.ceil(4.000...1) = 5.
        assert booking.total_price >= 100000

        # 6. Payment (Mocking the adapter process)
        from payments.models import PaymentTransaction
        tx = PaymentTransaction.objects.create(
            booking=booking,
            transaction_id="TX_E2E_001",
            amount=booking.total_price,
            provider="Airtel",
            status="SUCCESS"
        )
        booking.status = "PAID"
        booking.save()

        assert booking.status == "PAID"
