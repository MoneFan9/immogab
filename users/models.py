from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes KYC (Know Your Customer) fields for Gabonese CNI/Passport verification.
    """
    ID_CARD_TYPES = [
        ('CNI', 'Carte Nationale d\'Identité'),
        ('PASSPORT', 'Passeport'),
        ('RESIDENCE_PERMIT', 'Carte de Séjour'),
    ]

    id_card_number = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Numéro de pièce d'identité")
    id_card_type = models.CharField(max_length=20, choices=ID_CARD_TYPES, default='CNI', verbose_name="Type de pièce d'identité")
    is_kyc_verified = models.BooleanField(default=False, verbose_name="Statut de vérification KYC")

    def __str__(self):
        return self.username
