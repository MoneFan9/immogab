from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Includes KYC (Know Your Customer) fields for Gabonese CNI/Passport verification.
    """
    ID_CARD_TYPES = [
        ('CNI', _('Carte Nationale d\'Identité')),
        ('PASSPORT', _('Passeport')),
        ('RESIDENCE_PERMIT', _('Carte de Séjour')),
    ]

    id_card_number = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name=_("Numéro de pièce d'identité"))
    id_card_type = models.CharField(max_length=20, choices=ID_CARD_TYPES, default='CNI', verbose_name=_("Type de pièce d'identité"))
    is_kyc_verified = models.BooleanField(default=False, verbose_name=_("Statut de vérification KYC"))

    def __str__(self):
        return self.username
