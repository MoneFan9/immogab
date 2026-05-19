import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils import timezone
from bookings.models import Booking
from payments.models import PaymentTransaction as Payment
from payments.gateways import MockPaymentGateway
from payments.logic import calculate_revenue_split
from payments.tasks import simulate_mobile_money_webhook

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def test_booking(db, test_user):
    return Booking.objects.create(
        user=test_user,
        property_id=1,
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
    response = gateway.process_payment(
        booking=test_booking,
        amount=test_booking.total_price,
        currency='XAF',
        provider='Airtel Money'
    )

    assert response['status'] == 'initiated'
    payment = Payment.objects.get(reference=response['reference'])
    assert payment.status == 'PENDING'
    assert payment.amount == test_booking.total_price

    mock_task.assert_called_once_with(payment.id)

@pytest.mark.django_db
def test_simulate_webhook_task(test_booking, settings):
    settings.IMMOGAB_COMMISSION_RATE = Decimal('0.15')

    payment = Payment.objects.create(
        booking=test_booking,
        amount=Decimal('20000.00'),
        reference='REF123',
        provider='Moov Money',
        status='PENDING'
    )

    # Run the task synchronously for testing
    # We mock time.sleep to make it fast
    with pytest.MonkeyPatch().context() as mp:
        mp.setattr("time.sleep", lambda x: None)
        simulate_mobile_money_webhook(payment.id)

    payment.refresh_from_db()
    assert payment.status == 'SUCCESS'
    assert payment.commission_amount == Decimal('3000')
    assert payment.host_amount == Decimal('17000')

    test_booking.refresh_from_db()
    assert test_booking.status == 'PAID'
