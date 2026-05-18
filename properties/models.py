from django.db import models
from django.utils.translation import gettext_lazy as _

class Property(models.Model):
    class Province(models.TextChoices):
        ESTUAIRE = 'estuaire', _('Estuaire')
        HAUT_OGOOUE = 'haut_ogooue', _('Haut-Ogooué')
        MOYEN_OGOOUE = 'moyen_ogooue', _('Moyen-Ogooué')
        NGOUNIE = 'ngounie', _('Ngounié')
        NYANGA = 'nyanga', _('Nyanga')
        OGOOUE_IVINDO = 'ogooue_ivindo', _('Ogooué-Ivindo')
        OGOOUE_LOLO = 'ogooue_lolo', _('Ogooué-Lolo')
        OGOOUE_MARITIME = 'ogooue_maritime', _('Ogooué-Maritime')
        WOLEU_NTEM = 'woleu_ntem', _('Woleu-Ntem')

    class PropertyType(models.TextChoices):
        TERRAIN = 'terrain', _('Terrain')
        MAISON = 'maison', _('Maison')
        APPARTEMENT = 'appartement', _('Appartement')
        ESPACE_EVENEMENTIEL = 'espace_evenementiel', _('Espace Événementiel')

    title = models.CharField(_("Titre"), max_length=255)
    description = models.TextField(_("Description"))
    property_type = models.CharField(
        _("Type de bien"),
        max_length=50,
        choices=PropertyType.choices,
        db_index=True
    )
    province = models.CharField(
        _("Province"),
        max_length=50,
        choices=Province.choices,
        db_index=True
    )
    city = models.CharField(_("Ville"), max_length=100)
    neighborhood = models.CharField(_("Quartier"), max_length=100)
    address = models.TextField(_("Adresse"), blank=True, null=True)

    latitude = models.DecimalField(_("Latitude"), max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(_("Longitude"), max_digits=9, decimal_places=6, null=True, blank=True)

    price_per_hour = models.DecimalField(_("Prix par heure"), max_digits=10, decimal_places=0, null=True, blank=True, db_index=True)
    price_per_day = models.DecimalField(_("Prix par jour"), max_digits=10, decimal_places=0, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Propriété")
        verbose_name_plural = _("Propriétés")

    def __str__(self):
        return self.title
