import pytest
from django.utils import timezone
from datetime import timedelta
from core.models import User
from properties.models import Property
from bookings.models import Booking
from escrow.models import Escrow
from decimal import Decimal

@pytest.mark.django_db
class TestEscrowModel:
    def setup_method(self):
        self.user = User.objects.create_user(username="testuser_escrow", password="password")
        self.property = Property.objects.create(
            title="Escrow Villa",
            description="Villa for escrow test",
            property_type="villa",
            price=Decimal("10000.00"),
            address="456 Escrow Ave",
            city="Libreville",
            province="estuaire",
            owner=self.user
        )
        self.booking = Booking.objects.create(
            property=self.property,
            user=self.user,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=5)
        )

    def test_escrow_creation(self):
        escrow = Escrow.objects.create(
            booking=self.booking,
            amount=Decimal("50000.00")
        )
        assert escrow.booking == self.booking
        assert escrow.amount == Decimal("50000.00")
        assert escrow.is_frozen is True
        assert escrow.is_released is False

    def test_one_to_one_relationship(self):
        Escrow.objects.create(
            booking=self.booking,
            amount=Decimal("50000.00")
        )
        # Attempting to create another escrow for the same booking should fail
        with pytest.raises(Exception): # integrity error usually
             Escrow.objects.create(
                booking=self.booking,
                amount=Decimal("20000.00")
            )
