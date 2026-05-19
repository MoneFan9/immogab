from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Escrow
from .services import release_escrow
import logging

logger = logging.getLogger(__name__)

@shared_task
def schedule_escrow_release(escrow_id):
    """
    Task to be executed after the event ends (with a grace period).
    Checks for noise complaints and releases the escrow if none are found.
    """
    try:
        escrow = Escrow.objects.get(id=escrow_id)
        booking = escrow.booking

        # Grace period logic: 2 hours after end_time
        release_threshold = booking.end_time + timedelta(hours=2)

        if timezone.now() < release_threshold:
            logger.warning(f"Attempted to release escrow {escrow_id} before grace period ends.")
            return "Too early (grace period active)"

        if release_escrow(escrow):
            logger.info(f"Escrow {escrow_id} for booking {booking.id} released successfully.")
            return "Released"
        else:
            if escrow.status == Escrow.EscrowStatus.CLAIMED or escrow.has_noise_complaint:
                logger.info(f"Escrow {escrow_id} NOT released: noise complaint reported.")
                return "Blocked by noise complaint"
            return f"Status: {escrow.status}"

    except Escrow.DoesNotExist:
        logger.error(f"Escrow {escrow_id} does not exist.")
        return "Error"
