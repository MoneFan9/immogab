import time
from celery import shared_task
from django.conf import settings
from decimal import Decimal
from .models import Payment
from .logic import calculate_revenue_split

@shared_task
def simulate_mobile_money_webhook(payment_id):
    """
    Simulates the asynchronous nature of mobile money payments in Gabon.
    Wait for a few seconds, then update the payment status and split revenue.
    """
    try:
        payment = Payment.objects.get(id=payment_id)

        # Simulate network/provider delay
        time.sleep(2)

        # Calculate revenue split
        commission_rate = getattr(settings, 'IMMOGAB_COMMISSION_RATE', Decimal('0.15'))
        split = calculate_revenue_split(payment.amount, commission_rate)

        # Update payment
        payment.commission_amount = split['commission']
        payment.host_amount = split['host']
        payment.status = 'SUCCESS'
        payment.save()

        # Update booking status
        booking = payment.booking
        booking.status = 'PAID'
        booking.save()

        return f"Payment {payment_id} processed successfully."

    except Payment.DoesNotExist:
        return f"Payment {payment_id} not found."
    except Exception as e:
        return f"Error processing payment {payment_id}: {str(e)}"
