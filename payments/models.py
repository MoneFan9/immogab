from django.db import models
from bookings.models import Booking
from django.utils.translation import gettext_lazy as _

class PaymentTransaction(models.Model):
    class PaymentStatus(models.TextChoices):
        INITIATED = "INITIATED", _("Initié")
        SUCCESS = "SUCCESS", _("Réussi")
        FAILED = "FAILED", _("Échoué")

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="XAF")
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.INITIATED
    )
    provider = models.CharField(max_length=50, default="Mock")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
