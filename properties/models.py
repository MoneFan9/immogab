from django.db import models

class Property(models.Model):
    PROPERTY_TYPES = [
        ('villa', 'Villa'),
        ('appartement', 'Appartement'),
        ('terrain', 'Terrain'),
        ('bureau', 'Bureau'),
        ('espace_evenementiel', 'Espace Événementiel'),
        ('chambre', 'Chambre'),
    ]

    PROVINCE_CHOICES = [
        ('estuaire', 'Estuaire'),
        ('haut_ogooue', 'Haut-Ogooué'),
        ('moyen_ogooue', 'Moyen-Ogooué'),
        ('ngounie', 'Ngounié'),
        ('nyanga', 'Nyanga'),
        ('ogooue_ivindo', 'Ogooué-Ivindo'),
        ('ogooue_lolo', 'Ogooué-Lolo'),
        ('ogooue_maritime', 'Ogooué-Maritime'),
        ('woleu_ntem', 'Woleu-Ntem'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES, db_index=True)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, db_index=True)
    location = models.CharField(max_length=255)
    price_per_hour = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)

    def __str__(self):
        return self.title
