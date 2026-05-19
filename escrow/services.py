from django.utils import timezone
from .models import Escrow

def freeze_escrow(booking, amount):
    """
    Freezes the caution amount for a booking.
    """
    escrow, created = Escrow.objects.get_or_create(
        booking=booking,
        defaults={'amount': amount}
    )

    if escrow.status == Escrow.EscrowStatus.PENDING:
        escrow.status = Escrow.EscrowStatus.FROZEN
        escrow.frozen_at = timezone.now()
        escrow.save()

    return escrow

def release_escrow(escrow):
    """
    Releases the frozen caution if no noise complaints were reported.
    """
    if escrow.status == Escrow.EscrowStatus.FROZEN and not escrow.has_noise_complaint:
        escrow.status = Escrow.EscrowStatus.RELEASED
        escrow.released_at = timezone.now()
        escrow.save()
        return True
    return False

def claim_escrow(escrow):
    """
    Claims the escrow due to noise complaints.
    """
    if escrow.status == Escrow.EscrowStatus.FROZEN:
        escrow.status = Escrow.EscrowStatus.CLAIMED
        escrow.has_noise_complaint = True
        escrow.save()
        return True
    return False

def report_noise_complaint(escrow):
    """
    Flags the escrow due to noise complaints, preventing automatic release.
    Deprecated: use claim_escrow instead.
    """
    return claim_escrow(escrow)
