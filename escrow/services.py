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

    if not escrow.is_frozen:
        escrow.is_frozen = True
        escrow.frozen_at = timezone.now()
        escrow.save()

    return escrow

def release_escrow(escrow):
    """
    Releases the frozen caution if no noise complaints were reported.
    """
    if escrow.is_frozen and not escrow.is_released and not escrow.has_noise_complaint:
        escrow.is_released = True
        escrow.released_at = timezone.now()
        escrow.save()
        return True
    return False

def report_noise_complaint(escrow):
    """
    Flags the escrow due to noise complaints, preventing automatic release.
    """
    escrow.has_noise_complaint = True
    escrow.save()
    return True
