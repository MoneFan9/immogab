from django.db import models

class Property(models.Model):
    """
    Property model for ImmoGab.
    Includes Gabonese geolocation and support for hourly/daily pricing.
    """
    PROPERTY_TYPES = [
        ('TERRAIN', 'Terrain'),
        ('MAISON', 'Maison'),
        ('APPARTEMENT', 'Appartement'),
        ('ESPACE_EVENEMENTIEL', 'Espace Événementiel'),
    ]

    PROVINCES = [
        ('ESTUAIRE', 'Estuaire'),
        ('HAUT_OGOQUE', 'Haut-Ogooué'),
        ('MOYEN_OGOQUE', 'Moyen-Ogooué'),
        ('NGOUNIE', 'Ngounié'),
        ('NYANGA', 'Nyanga'),
        ('OGOOUE_IVINDO', 'Ogooué-Ivindo'),
        ('OGOOUE_LOLO', 'Ogooué-Lolo'),
        ('OGOOUE_MARITIME', 'Ogooué-Maritime'),
        ('WOLEU_NTEM', 'Woleu-Ntem'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)

    # Geolocation
    province = models.CharField(max_length=20, choices=PROVINCES)
    location = models.CharField(max_length=255, help_text="Ville, quartier ou adresse précise")

    # Pricing
    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    caution_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"

    def __str__(self):
        return self.title
