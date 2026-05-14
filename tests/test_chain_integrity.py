import pytest
from django.conf import settings
from datetime import datetime, timedelta

@pytest.mark.django_db
def test_end_to_end_chain_integrity():
    """
    This test simulates the full user journey: Search -> KYC -> Payment -> Jeedom.
    It expects real Django models and PostgreSQL (via Django ORM) to be used.
    """

    # 1. SEARCH BREAK: Expecting a real Property model from a 'properties' app
    try:
        from properties.models import Property
    except ImportError:
        pytest.fail("CHAIN BREAK: 'properties' app or 'Property' model is missing. README mandates modular architecture.")

    # Create a real property in the database
    prop = Property.objects.create(
        title="Villa à Libreville",
        location="Libreville",
        province="estuaire",
        property_type="villa",
        price_per_hour=5000
    )
    assert prop.id is not None

    # 2. KYC BREAK: Expecting a custom User model with KYC fields in 'core' app
    try:
        from core.models import User
    except ImportError:
        pytest.fail("CHAIN BREAK: 'core' app or custom 'User' model is missing. KYC fields are required by README.")

    user = User.objects.create_user(username="testguest", password="password123", id_card_number="GAB-12345")
    assert not user.is_kyc_verified

    # KYC Verification logic (should use real service/model updates)
    try:
        from immogab.services import validate_kyc
        validate_kyc(user)
        user.refresh_from_db()
        assert user.is_kyc_verified
    except (ImportError, AttributeError):
        pytest.fail("CHAIN BREAK: 'validate_kyc' service is missing or improperly implemented in 'immogab.services'.")

    # 3. BOOKING BREAK: Expecting 'bookings' app and real overlap checks against DB
    try:
        from bookings.models import Booking
    except ImportError:
        pytest.fail("CHAIN BREAK: 'bookings' app or 'Booking' model is missing.")

    start_time = datetime.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)

    booking = Booking.objects.create(
        user=user,
        property=prop,
        start_time=start_time,
        end_time=end_time,
        status="PENDING"
    )
    assert booking.id is not None

    # 4. PAYMENT BREAK: Expecting 'payments' logic and state sync
    try:
        from immogab.services import MockPaymentGateway
        gateway = MockPaymentGateway()
        payment_result = gateway.process_payment(amount=10000, currency="XAF", reference=f"BOOK-{booking.id}")

        if payment_result["status"] == "success":
            booking.status = "PAID"
            booking.save()

        booking.refresh_from_db()
        assert booking.status == "PAID"
    except (ImportError, AttributeError):
        pytest.fail("CHAIN BREAK: 'MockPaymentGateway' is missing or improperly implemented in 'immogab.services'.")

    # 5. JEEDOM BREAK: Final signal trigger
    try:
        from immogab.services import call_jeedom_webhook
        # In a real system, this might be triggered by a post_save signal or background task
        # For this test, we call it with a fake URL to ensure it handles connection errors as defined.
        with pytest.raises(ConnectionError):
             call_jeedom_webhook("http://fake-jeedom.local", "cmd-123", "api-key")
    except (ImportError, AttributeError):
        pytest.fail("CHAIN BREAK: 'call_jeedom_webhook' is missing or improperly implemented in 'immogab.services'.")

@pytest.mark.django_db
def test_database_engine_integrity():
    """
    Verify that PostgreSQL is being used as mandated by the README.
    """
    engine = settings.DATABASES['default']['ENGINE']
    assert "postgresql" in engine, f"CHAIN BREAK: Database engine is {engine}, but PostgreSQL is strictly mandatory."
