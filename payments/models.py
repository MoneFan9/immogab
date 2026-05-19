from django.db import models
from django.utils.translation import gettext_lazy as _
from bookings.models import Booking

class PaymentTransaction(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        SUCCESS = 'SUCCESS', _('Réussi')
        FAILED = 'FAILED', _('Échoué')

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(_("Montant"), max_digits=12, decimal_places=0)
    currency = models.CharField(_("Devise"), max_length=10, default="XAF")
    transaction_id = models.CharField(_("ID de transaction"), max_length=100, unique=True)
    external_reference = models.CharField(_("Référence externe"), max_length=100, blank=True, null=True)
    provider = models.CharField(_("Fournisseur"), max_length=50)
    phone_number = models.CharField(_("Numéro de téléphone"), max_length=20, blank=True, null=True)
    status = models.CharField(_("Statut"), max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    commission_amount = models.DecimalField(_("Commission ImmoGab"), max_digits=12, decimal_places=0, null=True, blank=True)
    host_amount = models.DecimalField(_("Montant Hôte"), max_digits=12, decimal_places=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Transaction de paiement")
        verbose_name_plural = _("Transactions de paiement")

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"

# Alias for backward compatibility if needed
Payment = PaymentTransaction
