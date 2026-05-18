from django.db import models
from django.utils.translation import gettext_lazy as _

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

    TYPE_CHOICES = [
        ('terrain', 'Terrain'),
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('espace_evenementiel', 'Espace Événementiel'),
    ]

    title = models.CharField(_("Titre"), max_length=255)
    description = models.TextField(_("Description"))
    property_type = models.CharField(_("Type de bien"), max_length=50, choices=TYPE_CHOICES, db_index=True)
    province = models.CharField(_("Province"), max_length=50, choices=PROVINCE_CHOICES, db_index=True)
    city = models.CharField(_("Ville"), max_length=100, db_index=True)
    neighborhood = models.CharField(_("Quartier"), max_length=100, db_index=True)

    price_per_hour = models.DecimalField(_("Prix par heure"), max_digits=10, decimal_places=0, null=True, blank=True, db_index=True)
    price_per_day = models.DecimalField(_("Prix par jour"), max_digits=10, decimal_places=0, null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Propriété")
        verbose_name_plural = _("Propriétés")

    def __str__(self):
        return self.title
