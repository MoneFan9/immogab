from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import math

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")

        # Double booking prevention
        overlapping_bookings = Booking.objects.filter(
            property=self.property,
            status='PAID',
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        if overlapping_bookings.exists():
            raise ValidationError("This property is already booked for the selected time slot.")

    def save(self, *args, **kwargs):
        # Calculate total price: every started hour is charged
        duration = self.end_time - self.start_time
        hours = math.ceil(duration.total_seconds() / 3600)
        self.total_price = hours * self.property.price_per_hour

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} - {self.property.title} by {self.user.username}"
