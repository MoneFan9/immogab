from django.db import models

class Escrow(models.Model):
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='escrow')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_frozen = models.BooleanField(default=False)
    is_released = models.BooleanField(default=False)
    has_noise_complaint = models.BooleanField(default=False)

    def __str__(self):
        return f"Escrow for Booking {self.booking.id}"
