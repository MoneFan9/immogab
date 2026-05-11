from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('TERRAIN', 'Terrain'),
        ('MAISON', 'Maison'),
        ('APPARTEMENT', 'Appartement'),
        ('ESPACE_EVENEMENTIEL', 'Espace Événementiel'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, db_index=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)

    # Location
    province = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title
