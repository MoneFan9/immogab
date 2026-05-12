from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Escrow

def freeze_escrow(booking, amount):
    """
    Freezes a caution (escrow) amount for a booking.
    """
    with transaction.atomic():
        escrow, created = Escrow.objects.get_or_create(
            booking=booking,
            defaults={'amount': Decimal(str(amount)), 'status': 'FROZEN'}
        )
        if not created:
            escrow.amount = Decimal(str(amount))
            escrow.status = 'FROZEN'
            escrow.save()
        return escrow

def release_escrow_logic(escrow):
    """
    Logic to release the frozen escrow if no issues were reported.
    """
    if escrow.status == 'FROZEN':
        with transaction.atomic():
            escrow.status = 'RELEASED'
            escrow.released_at = timezone.now()
            escrow.save()
            return True
    return False

def forfeit_escrow_logic(escrow):
    """
    Logic to forfeit the escrow in case of noise or damage.
    """
    if escrow.status == 'FROZEN':
        with transaction.atomic():
            escrow.status = 'FORFEITED'
            escrow.save()
            return True
    return False
