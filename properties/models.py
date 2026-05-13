from django.db import models

class Property(models.Model):
    """
    Model representing a property in Gabon.
    """
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
        ('bureau', 'Bureau'),
        ('espace_evenementiel', 'Espace Événementiel'),
        ('chambre', 'Chambre'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, verbose_name="Type de bien")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Prix")

    # Location fields
    address = models.CharField(max_length=255, verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, verbose_name="Province")

    # Geolocation
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitude")

    owner = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='properties', verbose_name="Propriétaire")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Propriété"
        verbose_name_plural = "Propriétés"
