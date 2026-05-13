from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model for ImmoGab.
    Includes KYC fields as per Gabonese regulations.
    """
    cni_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de CNI")
    is_kyc_verified = models.BooleanField(default=False, verbose_name="KYC Vérifié")
    kyc_document = models.FileField(upload_to='kyc_documents/', blank=True, null=True, verbose_name="Document KYC")

    def __str__(self):
        return self.username
