import math
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from properties.models import Property

class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        PAID = 'PAID', _('Payée')
        CONFIRMED = 'CONFIRMED', _('Confirmée')
        CANCELLED = 'CANCELLED', _('Annulée')
        COMPLETED = 'COMPLETED', _('Terminée')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField(_("Heure de début"))
    end_time = models.DateTimeField(_("Heure de fin"))
    total_price = models.DecimalField(_("Prix total"), max_digits=12, decimal_places=0, null=True, blank=True)
    status = models.CharField(_("Statut"), max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Réservation")
        verbose_name_plural = _("Réservations")

    def save(self, *args, **kwargs):
        if not self.total_price and self.start_time and self.end_time and self.property:
            duration = self.end_time - self.start_time
            # Using exact hours to match test expectations if necessary, or just fixing the test.
            # 4 hours exactly should be 4.
            hours = duration.total_seconds() / 3600
            # Let's keep math.ceil for business logic (every started hour is due)
            # but ensure we understand why 4 hours gave 125000 (5 hours?)
            self.total_price = math.ceil(hours) * self.property.price_per_hour
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} - {self.property.title}"
