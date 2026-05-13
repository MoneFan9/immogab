from django.db import models

class Property(models.Model):
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

    PROPERTY_TYPE_CHOICES = [
        ('villa', 'Villa'),
        ('appartement', 'Appartement'),
        ('terrain', 'Terrain'),
        ('espace_evenementiel', 'Espace Événementiel'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, db_index=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, db_index=True)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Properties"
