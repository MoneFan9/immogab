from rest_framework import serializers
from .models import Escrow

class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = '__all__'
