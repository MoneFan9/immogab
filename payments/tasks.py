import time
from celery import shared_task
from django.conf import settings
from decimal import Decimal
from .models import PaymentTransaction
from .logic import calculate_revenue_split

@shared_task
def simulate_mobile_money_webhook(transaction_db_id):
    """
    Simulates the asynchronous nature of mobile money payments in Gabon.
    Wait for a few seconds, then update the transaction status and split revenue.
    """
    try:
        tx = PaymentTransaction.objects.get(id=transaction_db_id)

        # Simulate network/provider delay
        time.sleep(2)

        # Calculate revenue split
        commission_rate = getattr(settings, 'IMMOGAB_COMMISSION_RATE', Decimal('0.15'))
        split = calculate_revenue_split(tx.amount, commission_rate)

        # Update transaction
        tx.commission_amount = split['commission']
        tx.host_amount = split['host']
        tx.status = 'SUCCESS'
        tx.save()

        # Update booking status
        if tx.booking:
            booking = tx.booking
            booking.status = 'PAID'
            booking.save()

        return f"Transaction {transaction_db_id} processed successfully."

    except PaymentTransaction.DoesNotExist:
        return f"Transaction {transaction_db_id} not found."
    except Exception as e:
        return f"Error processing transaction {transaction_db_id}: {str(e)}"
