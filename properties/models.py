from django.db import models

class Property(models.Model):
    """
    Property model for ImmoGab.
    Includes property type, pricing (hourly/daily), and Gabonese geolocation.
    """
    PROPERTY_TYPES = [
        ('MAISON', 'Maison'),
        ('APPARTEMENT', 'Appartement'),
        ('TERRAIN', 'Terrain'),
        ('ESPACE_EVENEMENTIEL', 'Espace Événementiel'),
    ]

    PROVINCES = [
        ('ESTUAIRE', 'Estuaire'),
        ('HAUT_OGOOUE', 'Haut-Ogooué'),
        ('MOYEN_OGOOUE', 'Moyen-Ogooué'),
        ('NGOUNIE', 'Ngounié'),
        ('NYANGA', 'Nyanga'),
        ('OGOOUE_IVINDO', 'Ogooué-Ivindo'),
        ('OGOOUE_LOLO', 'Ogooué-Lolo'),
        ('OGOOUE_MARITIME', 'Ogooué-Maritime'),
        ('WOLEU_NTEM', 'Woleu-Ntem'),
    ]

    title = models.CharField(max_length=255, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, default='APPARTEMENT', verbose_name="Type de bien")

    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix par heure")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Prix par jour")

    # Geolocation
    province = models.CharField(max_length=50, choices=PROVINCES, verbose_name="Province")
    city = models.CharField(max_length=100, verbose_name="Ville")
    neighborhood = models.CharField(max_length=100, verbose_name="Quartier")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"
