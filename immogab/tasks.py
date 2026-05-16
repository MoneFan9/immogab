import logging
from celery import shared_task
from .services import call_jeedom_webhook

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_jeedom_command(self, api_url, command, api_key):
    """
    Celery task to send a command to Jeedom.
    Handles retries if the service call fails.
    """
    try:
        logger.info(f"Sending command {command} to Jeedom at {api_url}")
        return call_jeedom_webhook(api_url, command, api_key)
    except Exception as exc:
        logger.error(f"Error sending command to Jeedom: {exc}. Retrying...")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
