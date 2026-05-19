from django.db import models
from django.utils.translation import gettext_lazy as _
from bookings.models import Booking

class Escrow(models.Model):
    class EscrowStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        FROZEN = 'FROZEN', _('Gelée')
        RELEASED = 'RELEASED', _('Libérée')
        CLAIMED = 'CLAIMED', _('Réclamée (Tapage)')

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='escrow')
    amount = models.DecimalField(_("Montant de la caution"), max_digits=12, decimal_places=0)
    status = models.CharField(
        _("Statut"),
        max_length=20,
        choices=EscrowStatus.choices,
        default=EscrowStatus.PENDING
    )
    has_noise_complaint = models.BooleanField(_("Tapage nocturne signalé"), default=False)

    frozen_at = models.DateTimeField(null=True, blank=True)
    released_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Caution (Escrow)")
        verbose_name_plural = _("Cautions (Escrow)")

    def __str__(self):
        return f"Escrow for Booking {self.booking_id}"
