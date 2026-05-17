from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class IDCardType(models.TextChoices):
        CNI = "CNI", _("Carte Nationale d'Identité")
        PASSPORT = "PASSPORT", _("Passeport")
        RESIDENCE_PERMIT = "RESIDENCE_PERMIT", _("Carte de Séjour")

    id_card_number = models.CharField(_("Numéro de pièce d'identité"), max_length=50, blank=True, null=True, unique=True)
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

class KYCDocument(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", _("En attente")
        VALIDATED = "VALIDATED", _("Validé")
        REJECTED = "REJECTED", _("Rejeté")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document = models.FileField(_("Document"), upload_to='kyc/')
    status = models.CharField(_("Statut"), max_length=20, choices=Status.choices, default=Status.PENDING)
    rejection_reason = models.TextField(_("Raison du rejet"), null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Document KYC")
        verbose_name_plural = _("Documents KYC")
