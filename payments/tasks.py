import time
from celery import shared_task
from django.conf import settings
from decimal import Decimal
from .models import PaymentTransaction
from .logic import calculate_revenue_split

@shared_task
def simulate_mobile_money_webhook(payment_pk):
    """
    Simulates the asynchronous nature of mobile money payments in Gabon.
    Wait for a few seconds, then update the payment status and split revenue.
    """
    try:
        tx = PaymentTransaction.objects.get(pk=payment_pk)

        # Simulate network/provider delay
        time.sleep(2)

        # Calculate revenue split
        commission_rate = getattr(settings, 'IMMOGAB_COMMISSION_RATE', Decimal('0.15'))
        split = calculate_revenue_split(tx.amount, commission_rate)

        # In a real scenario, we might store these in a separate Settlement model
        # For now, we update the transaction or just log it
        tx.status = 'SUCCESS'
        tx.save()

        # Update booking status
        if tx.booking:
            booking = tx.booking
            booking.status = 'PAID'
            booking.save()

        return f"Transaction {payment_pk} processed successfully."

    except PaymentTransaction.DoesNotExist:
        return f"Transaction {payment_pk} not found."
    except Exception as e:
        return f"Error processing transaction {payment_pk}: {str(e)}"
