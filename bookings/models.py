from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import math

class Booking(models.Model):
    """
    Model representing a reservation for a property.
    Supports hourly pricing.
    """
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('PAID', 'Payé'),
        ('CANCELLED', 'Annulé'),
        ('FAILED', 'Échoué'),
    ]

    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Propriété"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Utilisateur"))

    start_time = models.DateTimeField(verbose_name=_("Date et heure de début"))
    end_time = models.DateTimeField(verbose_name=_("Date et heure de fin"))

    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Prix total"), null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name=_("Statut"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Validate that start_time is before end_time and that there are no overlaps.
        """
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(_("La date de début doit être antérieure à la date de fin."))

            # Overlap check
            overlapping_bookings = Booking.objects.filter(
                property=self.property,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError(_("Cette propriété est déjà réservée pour cette période."))

    def calculate_total_price(self):
        """
        Calculates the total price based on hourly rate.
        Each started hour is counted as a full hour.
        """
        if self.start_time and self.end_time and self.property and self.property.price_per_hour:
            duration = self.end_time - self.start_time
            hours = math.ceil(duration.total_seconds() / 3600)
            return self.property.price_per_hour * hours
        return 0

    def save(self, *args, **kwargs):
        if self.total_price is None:
            self.total_price = self.calculate_total_price()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Réservation {self.id} - {self.property.title} par {self.user.username}"

    class Meta:
        verbose_name = _("Réservation")
        verbose_name_plural = _("Réservations")
