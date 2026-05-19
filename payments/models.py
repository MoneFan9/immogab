from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class PaymentTransaction(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        SUCCESS = 'SUCCESS', _('Réussi')
        FAILED = 'FAILED', _('Échoué')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='XAF')
    transaction_id = models.CharField(max_length=100, unique=True)
    external_reference = models.CharField(max_length=100, null=True, blank=True)
    provider = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Transaction de paiement")
        verbose_name_plural = _("Transactions de paiement")

    def __str__(self):
        return f"{self.provider} - {self.transaction_id} ({self.status})"
