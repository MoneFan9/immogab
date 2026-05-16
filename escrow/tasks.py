from celery import shared_task
from django.utils import timezone
from .models import Escrow
from .services import release_escrow
import logging

logger = logging.getLogger(__name__)

@shared_task
def schedule_escrow_release(escrow_id):
    """
    Task to be executed after the event ends.
    Checks for noise complaints and releases the escrow if none are found.
    """
    try:
        escrow = Escrow.objects.get(id=escrow_id)

        # In a real scenario, this task would be scheduled to run at escrow.booking.end_time
        # For the purpose of this refined logic, we check if the event is indeed over
        if timezone.now() < escrow.booking.end_time:
            logger.warning(f"Attempted to release escrow {escrow_id} before booking end time.")
            return "Too early"

        if release_escrow(escrow):
            logger.info(f"Escrow {escrow_id} released successfully.")
            return "Released"
        else:
            if escrow.has_noise_complaint:
                logger.info(f"Escrow {escrow_id} NOT released due to noise complaint.")
                return "Blocked by noise complaint"
            return "Already released or not frozen"

    except Escrow.DoesNotExist:
        logger.error(f"Escrow {escrow_id} does not exist.")
        return "Error"
