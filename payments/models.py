from django.db import models
import uuid

class PaymentTransaction(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        SUCCESS = 'SUCCESS', 'Réussi'
        FAILED = 'FAILED', 'Échoué'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='XAF')
    transaction_id = models.CharField(max_length=100, unique=True)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction de Paiement'
        verbose_name_plural = 'Transactions de Paiement'

class Payment(models.Model):
    # Legacy model used in some services
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
