from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class IDCardType(models.TextChoices):
        CNI = "CNI", _("Carte Nationale d'Identité")
        PASSPORT = "PASSPORT", _("Passeport")
        RESIDENCE_PERMIT = "RESIDENCE_PERMIT", _("Carte de Séjour")

    id_card_number = models.CharField(_("Numéro de pièce d'identité"), max_length=50, blank=True, null=True)
    id_card_type = models.CharField(
        _("Type de pièce d'identité"),
        max_length=20,
        choices=IDCardType.choices,
        default=IDCardType.CNI
    )
    is_kyc_verified = models.BooleanField(_("Vérification KYC effectuée"), default=False)

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")

    def __str__(self):
        return self.username
