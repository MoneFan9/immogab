import pytest
from decimal import Decimal
from unittest.mock import patch
from django.conf import settings
from payments.gateways.mock import MockPaymentGateway
from payments.utils import calculate_revenue_split
from payments.tasks import simulate_mobile_money_callback

def test_revenue_split_calculation_default():
    # Default is 15%
    total = Decimal('100000') # 100 000 FCFA
    commission, payout = calculate_revenue_split(total)

    assert commission == Decimal('15000')
    assert payout == Decimal('85000')
    assert commission + payout == total

def test_revenue_split_rounding():
    # Test rounding with a complex amount
    # 15% of 100005 is 15000.75 -> should round to 15001
    total = Decimal('100005')
    commission, payout = calculate_revenue_split(total)

    assert commission == Decimal('15001')
    assert payout == Decimal('85004')
    assert commission + payout == total

def test_revenue_split_custom_rate(settings):
    # Test with 10% commission
    settings.IMMOGAB_COMMISSION_PERCENTAGE = '10.0'
    total = Decimal('200000')
    commission, payout = calculate_revenue_split(total)

    assert commission == Decimal('20000')
    assert payout == Decimal('180000')

@patch('payments.tasks.simulate_mobile_money_callback.delay')
def test_mock_payment_gateway_initiation(mock_delay):
    gateway = MockPaymentGateway()
    amount = 50000
    reference = "TEST-REF-1"

    result = gateway.process_payment(amount=amount, currency="XAF", reference=reference)

    assert result["status"] == "initiated"
    assert result["amount"] == amount
    assert result["reference"] == reference

    # Check if Celery task was triggered
    mock_delay.assert_called_once_with(
        transaction_id=result["transaction_id"],
        amount=float(amount),
        currency="XAF",
        reference=reference
    )

def test_async_task_simulation():
    # Run the task synchronously for testing
    transaction_id = "fake-uuid"
    amount = 25000.0
    currency = "XAF"
    reference = "BOOK-999"

    # We use .run() or just call it directly to bypass Celery infra during unit test if needed,
    # but here we just call the function.
    result = simulate_mobile_money_callback(transaction_id, amount, currency, reference)

    assert result["status"] == "success"
    assert result["transaction_id"] == transaction_id
    assert result["amount"] == amount
