from django.db import models
from django.utils.translation import gettext_lazy as _

class Property(models.Model):
    """
    Model representing a property in Gabon.
    """
    PROVINCE_CHOICES = [
        ('estuaire', _('Estuaire')),
        ('haut_ogooue', _('Haut-Ogooué')),
        ('moyen_ogooue', _('Moyen-Ogooué')),
        ('ngounie', _('Ngounié')),
        ('nyanga', _('Nyanga')),
        ('ogooue_ivindo', _('Ogooué-Ivindo')),
        ('ogooue_lolo', _('Ogooué-Lolo')),
        ('ogooue_maritime', _('Ogooué-Maritime')),
        ('woleu_ntem', _('Woleu-Ntem')),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('villa', _('Villa')),
        ('appartement', _('Appartement')),
        ('terrain', _('Terrain')),
        ('bureau', _('Bureau')),
        ('espace_evenementiel', _('Espace Événementiel')),
        ('chambre', _('Chambre')),
    ]

    title = models.CharField(max_length=200, verbose_name=_("Titre"))
    description = models.TextField(verbose_name=_("Description"))
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, verbose_name=_("Type de bien"), db_index=True)
    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Prix par heure"))

    # Location fields
    address = models.CharField(max_length=255, verbose_name=_("Adresse"))
    city = models.CharField(max_length=100, verbose_name=_("Ville"))
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, verbose_name=_("Province"), db_index=True)

    # Geolocation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_("Latitude"))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name=_("Longitude"))

    owner = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='properties', verbose_name=_("Propriétaire"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Propriété")
        verbose_name_plural = _("Propriétés")
