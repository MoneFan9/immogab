from django.db import models
from django.conf import settings
from properties.models import Property
from django.utils.translation import gettext_lazy as _

class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", _("En attente")
        PAID = "PAID", _("Payé")
        CANCELLED = "CANCELLED", _("Annulé")
        COMPLETED = "COMPLETED", _("Terminé")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="bookings")

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )

    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.property.title} by {self.user.username}"

class Escrow(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="escrow")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_frozen = models.BooleanField(default=True)
    is_released = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
