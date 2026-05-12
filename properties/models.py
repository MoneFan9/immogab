from django.db import models

class Property(models.Model):
    PROVINCE_CHOICES = [
        ('ESTUAIRE', 'Estuaire'),
        ('HAUT-OGOOUÉ', 'Haut-Ogooué'),
        ('MOYEN-OGOOUÉ', 'Moyen-Ogooué'),
        ('NGOUNIÉ', 'Ngounié'),
        ('NYANGA', 'Nyanga'),
        ('OGOOUÉ-IVINDO', 'Ogooué-Ivindo'),
        ('OGOOUÉ-LOLO', 'Ogooué-Lolo'),
        ('OGOOUÉ-MARITIME', 'Ogooué-Maritime'),
        ('WOLEU-NTEM', 'Woleu-Ntem'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('TERRAIN', 'Terrain'),
        ('MAISON', 'Maison'),
        ('APPARTEMENT', 'Appartement'),
        ('ESPACE_EVENEMENTIEL', 'Espace Événementiel'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, db_index=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    caution_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, db_index=True)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
