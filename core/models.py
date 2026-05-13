from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model for ImmoGab with KYC fields.
    """
    id_card_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Numéro de carte d'identité"))
    is_kyc_verified = models.BooleanField(default=False, verbose_name=_("KYC Vérifié"))
    kyc_document = models.FileField(upload_to='kyc_documents/', blank=True, null=True, verbose_name=_("Document KYC"))

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
