from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from properties.models import Property

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', _('En attente')),
        ('PAID', _('Payée')),
        ('CONFIRMED', _('Confirmée')),
        ('CANCELLED', _('Annulée')),
        ('COMPLETED', _('Terminée')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField(_("Heure de début"))
    end_time = models.DateTimeField(_("Heure de fin"))
    total_price = models.DecimalField(_("Prix total"), max_digits=12, decimal_places=0, null=True, blank=True)
    status = models.CharField(_("Statut"), max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Réservation")
        verbose_name_plural = _("Réservations")

    def __str__(self):
        return f"Booking {self.id} - {self.property.title}"
