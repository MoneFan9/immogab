from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id_card_number = models.CharField(max_length=50, blank=True, null=True)
    is_kyc_verified = models.BooleanField(default=False)
    kyc_document = models.FileField(upload_to='kyc_documents/', blank=True, null=True)

    def __str__(self):
        return self.username
