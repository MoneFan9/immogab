from django.db import models
from django.utils.translation import gettext_lazy as _

class Escrow(models.Model):
    """
    Model for managing security deposits (cautions) related to bookings.
    Includes anti-noise complaint logic.
    """
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='escrow', verbose_name=_("Réservation"))
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Montant de la caution"))

    is_frozen = models.BooleanField(default=True, verbose_name=_("Gelé"))
    is_released = models.BooleanField(default=False, verbose_name=_("Libéré"))

    # New field for anti-noise complaint
    has_noise_complaint = models.BooleanField(default=False, verbose_name=_("Plainte pour tapage nocturne"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def can_be_released(self):
        """
        Check if the escrow can be released.
        Release is forbidden if there is a noise complaint.
        """
        return not self.has_noise_complaint

    def release(self):
        """
        Release the escrow if no noise complaint is present.
        """
        if self.can_be_released():
            self.is_released = True
            self.is_frozen = False
            self.save()
            return True
        return False

    def __str__(self):
        status = "Libéré" if self.is_released else ("Bloqué (Tapage)" if self.has_noise_complaint else ("Gelé" if self.is_frozen else "Inactif"))
        return f"Caution {self.id} for Booking {self.booking_id} - {status}"

    class Meta:
        verbose_name = _("Caution (Escrow)")
        verbose_name_plural = _("Cautions (Escrows)")
