from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class IDCardType(models.TextChoices):
        CNI = 'CNI', _('Carte Nationale d\'Identité')
        PASSPORT = 'PASSPORT', _('Passeport')
        RESIDENCE_PERMIT = 'RESIDENCE_PERMIT', _('Carte de Séjour')

    id_card_number = models.CharField(_('ID Card Number'), max_length=50, blank=True, null=True)
    id_card_type = models.CharField(
        _('ID Card Type'),
        max_length=20,
        choices=IDCardType.choices,
        blank=True,
        null=True
    )
    is_kyc_verified = models.BooleanField(_('Is KYC Verified'), default=False)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class KYCDocument(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('En attente')
        VALIDATED = 'VALIDATED', _('Validé')
        REJECTED = 'REJECTED', _('Rejeté')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document = models.FileField(upload_to='kyc_documents/')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"KYC Document for {self.user.username} - {self.status}"
