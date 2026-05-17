import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from bookings.models import Booking
from payments.models import PaymentTransaction
from payments.gateways import MockPaymentGateway
from payments.logic import calculate_revenue_split
from payments.tasks import simulate_mobile_money_webhook
from properties.models import Property

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def test_property(db):
    return Property.objects.create(
        title="Test Property",
        province="estuaire",
        property_type="maison"
    )

@pytest.fixture
def test_booking(db, test_user, test_property):
    return Booking.objects.create(
        user=test_user,
        property=test_property,
        start_time=timezone.now(),
        end_time=timezone.now() + timezone.timedelta(hours=2),
        total_price=Decimal('20000.00'),
        status='PENDING'
    )

def test_revenue_split_logic():
    # 15% of 20000 is 3000
    result = calculate_revenue_split(Decimal('20000'), Decimal('0.15'))
    assert result['commission'] == Decimal('3000')
    assert result['host'] == Decimal('17000')
    assert result['total'] == result['commission'] + result['host']

    # Case with rounding (5555 * 0.15 = 833.25 -> 833)
    result = calculate_revenue_split(Decimal('5555'), Decimal('0.15'))
    assert result['commission'] == Decimal('833')
    assert result['host'] == Decimal('4722')
    assert result['total'] == Decimal('5555')

@pytest.mark.django_db
def test_mock_gateway_initiation(test_booking, mocker):
    # Mock the celery task to avoid actual delay and background processing in unit test
    mock_task = mocker.patch('payments.tasks.simulate_mobile_money_webhook.delay')

    gateway = MockPaymentGateway()
    # In the new gateways.py, process_payment takes (booking, amount, currency="XAF")
    response = gateway.process_payment(
        booking=test_booking,
        amount=test_booking.total_price,
        currency='XAF'
    )

    assert response['status'] == 'success'
    tx = PaymentTransaction.objects.get(transaction_id=response['transaction_id'])
    assert tx.status == 'SUCCESS'
    assert tx.amount == test_booking.total_price

    # In gateways.py, simulate_mobile_money_webhook.delay is NOT called, it calls synchronize_payment_status instead
    # So we don't assert mock_task.assert_called_once_with(...)
