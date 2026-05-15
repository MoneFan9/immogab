from django.db import models
from django.utils.translation import gettext_lazy as _

class Property(models.Model):
    class PropertyType(models.TextChoices):
        MAISON = 'MAISON', _('Maison')
        APPARTEMENT = 'APPARTEMENT', _('Appartement')
        TERRAIN = 'TERRAIN', _('Terrain')
        ESPACE_EVENEMENTIEL = 'ESPACE_EVENEMENTIEL', _('Espace Événementiel')

    class Province(models.TextChoices):
        ESTUAIRE = 'Estuaire', _('Estuaire')
        HAUT_OGOOUE = 'Haut-Ogooué', _('Haut-Ogooué')
        MOYEN_OGOOUE = 'Moyen-Ogooué', _('Moyen-Ogooué')
        NGOUNIE = 'Ngounié', _('Ngounié')
        NYANGA = 'Nyanga', _('Nyanga')
        OGOOUE_IVINDO = 'Ogooué-Ivindo', _('Ogooué-Ivindo')
        OGOOUE_LOLO = 'Ogooué-Lolo', _('Ogooué-Lolo')
        OGOOUE_MARITIME = 'Ogooué-Maritime', _('Ogooué-Maritime')
        WOLEU_NTEM = 'Woleu-Ntem', _('Woleu-Ntem')

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(
        max_length=50,
        choices=PropertyType.choices,
        db_index=True
    )
    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True)
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True)

    province = models.CharField(
        max_length=50,
        choices=Province.choices,
        db_index=True
    )
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Propriété')
        verbose_name_plural = _('Propriétés')

    def __str__(self):
        return self.title
