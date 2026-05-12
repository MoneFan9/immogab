from django.db import models
from bookings.models import Booking

class Escrow(models.Model):
    STATUS_CHOICES = [
        ('FROZEN', 'Frozen'),
        ('RELEASED', 'Released'),
        ('FORFEITED', 'Forfeited'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='escrow')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='FROZEN', db_index=True)
    frozen_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Escrow for {self.booking}"
