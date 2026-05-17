from django.db import models
from django.utils.translation import gettext_lazy as _
from bookings.models import Booking
from django.utils import timezone

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

    def save(self, *args, **kwargs):
        if self.amount > 0 and not self.is_frozen and not self.frozen_at and not self.is_released:
            self.is_frozen = True
            self.frozen_at = timezone.now()
        super().save(*args, **kwargs)

    def can_be_released(self):
        return not self.is_released and not self.has_noise_complaint

    def release(self):
        if self.can_be_released():
            self.is_released = True
            self.is_frozen = False
            self.released_at = timezone.now()
            self.save()
            return True
        return False

    def __str__(self):
        return f"Escrow for Booking {self.booking_id}"
