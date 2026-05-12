from celery import shared_task
from django.utils import timezone
from .models import Escrow
from .services import release_escrow_logic, forfeit_escrow_logic
from bookings.models import Booking

@shared_task
def release_escrow_after_event(booking_id):
    """
    Asynchronous task to check if an escrow should be released or forfeited
    after an event based on whether noise was reported.
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        escrow = booking.escrow

        if escrow.status != 'FROZEN':
            return f"Escrow for booking {booking_id} is not in FROZEN state."

        # Logic: If noise was reported, forfeit. Otherwise, release.
        if booking.has_noise_report:
            forfeit_escrow_logic(escrow)
            return f"Escrow for booking {booking_id} FORFEITED due to noise report."
        else:
            release_escrow_logic(escrow)
            return f"Escrow for booking {booking_id} RELEASED successfully."

    except Booking.DoesNotExist:
        return f"Booking {booking_id} does not exist."
    except Escrow.DoesNotExist:
        return f"Escrow for booking {booking_id} does not exist."
    except Exception as e:
        return f"Error processing escrow for booking {booking_id}: {str(e)}"
