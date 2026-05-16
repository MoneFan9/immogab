from django.db import models
from django.utils.translation import gettext_lazy as _

class Property(models.Model):
    class PropertyType(models.TextChoices):
        TERRAIN = "TERRAIN", _("Terrain")
        MAISON = "MAISON", _("Maison")
        APPARTEMENT = "APPARTEMENT", _("Appartement")
        ESPACE_EVENEMENTIEL = "ESPACE_EVENEMENTIEL", _("Espace Événementiel")

    class Province(models.TextChoices):
        ESTUAIRE = "ESTUAIRE", _("Estuaire")
        HAUT_OGOOUE = "HAUT_OGOOUE", _("Haut-Ogooué")
        MOYEN_OGOOUE = "MOYEN_OGOOUE", _("Moyen-Ogooué")
        NGOUNIE = "NGOUNIE", _("Ngounié")
        NYANGA = "NYANGA", _("Nyanga")
        OGO_IVINDO = "OGO_IVINDO", _("Ogooué-Ivindo")
        OGO_LOLO = "OGO_LOLO", _("Ogooué-Lolo")
        OGO_MARITIME = "OGO_MARITIME", _("Ogooué-Maritime")
        WOLEU_NTEM = "WOLEU_NTEM", _("Woleu-Ntem")

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.APPARTEMENT
    )
    province = models.CharField(
        max_length=20,
        choices=Province.choices,
        default=Province.ESTUAIRE
    )
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)

    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
