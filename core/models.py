from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id_card_number = models.CharField(max_length=50, blank=True, null=True)
    is_kyc_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
