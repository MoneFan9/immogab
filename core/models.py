from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    id_card_number = models.CharField(_("Numéro de pièce d'identité"), max_length=50, unique=True, null=True, blank=True)
    id_card_type = models.CharField(_("Type de pièce d'identité"), max_length=50, null=True, blank=True)
    is_kyc_verified = models.BooleanField(_("Vérification KYC effectuée"), default=False)

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
