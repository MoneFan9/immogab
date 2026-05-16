from rest_framework import serializers
from .models import Booking
from properties.models import Property

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'property', 'start_time', 'end_time', 'total_price', 'status']
        read_only_fields = ['total_price', 'status']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("L'heure de début doit être antérieure à l'heure de fin.")
        return data
