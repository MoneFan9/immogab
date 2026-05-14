import requests
import time
from celery import shared_task
from django.urls import reverse
from django.conf import settings

@shared_task
def simulate_payment_webhook(transaction_id, amount, currency, reference):
    """
    Simulates the external payment provider calling our webhook.
    Wait for a few seconds to mimic processing time.
    """
    # In eager mode (testing), we don't want to actually sleep if possible,
    # but for a simulation it's okay.
    if not getattr(settings, 'CELERY_TASK_ALWAYS_EAGER', False):
        time.sleep(2)

    # Construct the webhook URL
    # Note: In a real environment, this would need to be a fully qualified URL.
    # For simulation, we'll try to post to our local endpoint if a base URL is provided.
    webhook_path = reverse('payments:mock-webhook')

    # We use a placeholder base URL if not set
    base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    webhook_url = f"{base_url}{webhook_path}"

    payload = {
        "status": "success",
        "transaction_id": transaction_id,
        "amount": amount,
        "currency": currency,
        "reference": reference
    }

    try:
        # In this mock environment, we might just call the view function directly
        # or use requests if the server is running.
        # For the purpose of this task, we'll simulate the call by sending a POST request.
        # If it fails (e.g. server not running), we'll at least log it.
        response = requests.post(webhook_url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        # For testing, we can also manually trigger the processing logic
        # instead of a real HTTP request if we are in a test environment.
        print(f"Webhook simulation failed: {e}")
        return False
