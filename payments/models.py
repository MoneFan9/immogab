from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class PaymentTransaction(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        SUCCESS = 'SUCCESS', _('Réussi')
        FAILED = 'FAILED', _('Échoué')

    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='XAF')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    host_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    provider = models.CharField(max_length=50)
    external_reference = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"

class Payment(models.Model):
    # Re-adding Payment model as it seems to be used by some tasks/services
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='legacy_payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    host_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('PENDING', _('En attente')),
            ('SUCCESS', _('Réussi')),
            ('FAILED', _('Échoué')),
        ],
        default='PENDING'
    )
    reference = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
