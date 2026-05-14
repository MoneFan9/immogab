from celery import shared_task
from django.db import transaction
from .models import Escrow

@shared_task
def release_escrow_task(escrow_id):
    """
    Asynchronous task to release escrow 24h after the event.
    Only releases if no noise complaint was reported.
    """
    with transaction.atomic():
        try:
            escrow = Escrow.objects.select_for_update().get(id=escrow_id)

            if escrow.is_released:
                return f"Escrow {escrow_id} already released."

            if escrow.has_noise_complaint:
                # If there's a complaint, escrow remains frozen for manual review/fine processing
                return f"Escrow {escrow_id} remains frozen due to noise complaint."

            escrow.is_released = True
            escrow.is_frozen = False
            escrow.save()

            return f"Escrow {escrow_id} successfully released."

        except Escrow.DoesNotExist:
            return f"Escrow {escrow_id} does not exist."
