from django.db import models
from django.utils.translation import gettext_lazy as _
from bookings.models import Booking

class Escrow(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='escrow')
    amount = models.DecimalField(_("Montant de la caution"), max_digits=12, decimal_places=0)
    is_frozen = models.BooleanField(_("Est gelée"), default=False)
    is_released = models.BooleanField(_("Est libérée"), default=False)
    has_noise_complaint = models.BooleanField(_("Tapage nocturne signalé"), default=False)

    frozen_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Caution (Escrow)")
        verbose_name_plural = _("Cautions (Escrow)")

    def __str__(self):
        return f"Escrow for Booking {self.booking_id}"
