from django.db import transaction
from payments.gateways import MockPaymentGateway
from .models import Booking

def process_booking_payment(booking_id):
    """
    Simulates payment processing for a booking and updates its status.
    """
    try:
        with transaction.atomic():
            booking = Booking.objects.select_for_update().get(id=booking_id)

            if booking.status != 'PENDING':
                return booking

            gateway = MockPaymentGateway()
            payment_result = gateway.process_payment(
                amount=float(booking.total_price),
                currency="XAF",
                reference=f"BOOK-{booking.id}"
            )

            if payment_result['status'] == 'success':
                booking.status = 'PAID'
            else:
                booking.status = 'FAILED'

            booking.save()
            return booking
    except Booking.DoesNotExist:
        return None
