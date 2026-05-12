from celery import shared_task
import time
import logging

logger = logging.getLogger(__name__)

@shared_task
def simulate_mobile_money_callback(transaction_id, amount, currency, reference):
    """
    Simulates the asynchronous callback from a mobile money provider in Gabon.
    Wait a few seconds to mimic user interaction (OTP entry).
    """
    logger.info(f"Starting async simulation for transaction {transaction_id}")

    # Simulate wait for user to receive SMS and enter OTP on their phone
    time.sleep(2)

    # In a real app, this would update the Booking/Payment model in the DB
    # or call a webhook endpoint.
    logger.info(f"Transaction {transaction_id} successfully validated via Mobile Money Gabon simulation.")

    return {
        "transaction_id": transaction_id,
        "status": "success",
        "amount": amount,
        "currency": currency,
        "reference": reference
    }
