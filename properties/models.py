from django.db import models

class Property(models.Model):
    PROVINCE_CHOICES = [
        ('Estuaire', 'Estuaire'),
        ('Haut-Ogooué', 'Haut-Ogooué'),
        ('Moyen-Ogooué', 'Moyen-Ogooué'),
        ('Ngounié', 'Ngounié'),
        ('Nyanga', 'Nyanga'),
        ('Ogooué-Ivindo', 'Ogooué-Ivindo'),
        ('Ogooué-Lolo', 'Ogooué-Lolo'),
        ('Ogooué-Maritime', 'Ogooué-Maritime'),
        ('Woleu-Ntem', 'Woleu-Ntem'),
    ]

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    type = models.CharField(max_length=50)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return self.title
