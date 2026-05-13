from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model for ImmoGab.
    Includes KYC fields for CNI (Carte Nationale d'Identité).
    """
    cni_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de CNI")
    is_kyc_verified = models.BooleanField(default=False, verbose_name="Vérifié par KYC")
    kyc_document = models.FileField(upload_to="kyc_documents/", blank=True, null=True, verbose_name="Document KYC")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numéro de téléphone")

    def __str__(self):
        return self.username
