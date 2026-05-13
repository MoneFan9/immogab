from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'property', 'user', 'start_time', 'end_time',
            'total_price', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_price', 'status', 'user']

    def validate(self, data):
        """
        Extra validation if needed.
        Most logic is already in the model's clean() method.
        """
        return data
