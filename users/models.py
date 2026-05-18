from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class IDCardType(models.TextChoices):
        CNI = "CNI", _("Carte Nationale d'Identité")
        PASSPORT = "PASSPORT", _("Passeport")
        RESIDENCE_PERMIT = "RESIDENCE_PERMIT", _("Carte de Séjour")

    id_card_number = models.CharField(
        _("Numéro de pièce d'identité"),
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kyc_documents", verbose_name=_("Utilisateur"))
    document_type = models.CharField(
        _("Type de document"),
        max_length=20,
        choices=User.IDCardType.choices
    )
    document_file = models.FileField(_("Fichier du document"), upload_to="kyc_documents/")
    status = models.CharField(
        _("Statut"),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    submitted_at = models.DateTimeField(_("Soumis le"), auto_now_add=True)
    reviewed_at = models.DateTimeField(_("Revu le"), null=True, blank=True)
    rejection_reason = models.TextField(_("Raison du rejet"), blank=True, null=True)

    class Meta:
        verbose_name = _("Document KYC")
        verbose_name_plural = _("Documents KYC")

    def __str__(self):
        return f"{self.user.username} - {self.document_type} ({self.status})"
