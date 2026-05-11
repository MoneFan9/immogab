from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('TERRAIN', 'Terrain'),
        ('MAISON', 'Maison'),
        ('APPARTEMENT', 'Appartement'),
        ('ESPACE_EVENEMENTIEL', 'Espace Événementiel'),
    ]

    PROVINCES = [
        ('ESTUAIRE', 'Estuaire'),
        ('HAUT_OGOOUÉ', 'Haut-Ogooué'),
        ('MOYEN_OGOOUÉ', 'Moyen-Ogooué'),
        ('NGOUNIÉ', 'Ngounié'),
        ('NYANGA', 'Nyanga'),
        ('OGOOUÉ_IVINDO', 'Ogooué-Ivindo'),
        ('OGOOUÉ_LOLO', 'Ogooué-Lolo'),
        ('OGOOUÉ_MARITIME', 'Ogooué-Maritime'),
        ('WOLEU_NTEM', 'Woleu-Ntem'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, db_index=True)

    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True)
    price_per_day = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, db_index=True)

    province = models.CharField(max_length=50, choices=PROVINCES, db_index=True)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Properties"
