from django.db import models
from django.utils.translation import gettext_lazy as _

class Property(models.Model):
    """
    Property model for ImmoGab.
    Includes property type, pricing (hourly/daily), and Gabonese geolocation.
    """
    PROPERTY_TYPES = [
        ('MAISON', _('Maison')),
        ('APPARTEMENT', _('Appartement')),
        ('TERRAIN', _('Terrain')),
        ('ESPACE_EVENEMENTIEL', _('Espace Événementiel')),
    ]

    PROVINCES = [
        ('ESTUAIRE', _('Estuaire')),
        ('HAUT_OGOOUE', _('Haut-Ogooué')),
        ('MOYEN_OGOOUE', _('Moyen-Ogooué')),
        ('NGOUNIE', _('Ngounié')),
        ('NYANGA', _('Nyanga')),
        ('OGOOUE_IVINDO', _('Ogooué-Ivindo')),
        ('OGOOUE_LOLO', _('Ogooué-Lolo')),
        ('OGOOUE_MARITIME', _('Ogooué-Maritime')),
        ('WOLEU_NTEM', _('Woleu-Ntem')),
    ]

    title = models.CharField(max_length=255, verbose_name=_("Titre"))
    description = models.TextField(verbose_name=_("Description"))
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='APPARTEMENT', verbose_name=_("Type de bien"))

    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Prix par heure"))
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_("Prix par jour"))

    # Geolocation
    province = models.CharField(max_length=50, choices=PROVINCES, verbose_name=_("Province"))
    city = models.CharField(max_length=100, verbose_name=_("Ville"))
    neighborhood = models.CharField(max_length=100, verbose_name=_("Quartier"))
    latitude = models.FloatField(null=True, blank=True, verbose_name=_("Latitude"))
    longitude = models.FloatField(null=True, blank=True, verbose_name=_("Longitude"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Propriété")
        verbose_name_plural = _("Propriétés")
