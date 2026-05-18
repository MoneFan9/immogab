from django_filters import rest_framework as filters
from .models import Property

class PropertyFilter(filters.FilterSet):
    min_price_day = filters.NumberFilter(field_name="price_per_day", lookup_expr='gte')
    max_price_day = filters.NumberFilter(field_name="price_per_day", lookup_expr='lte')
    min_price_hour = filters.NumberFilter(field_name="price_per_hour", lookup_expr='gte')
    max_price_hour = filters.NumberFilter(field_name="price_per_hour", lookup_expr='lte')

    class Meta:
        model = Property
        fields = {
            'province': ['exact'],
            'property_type': ['exact'],
            'city': ['icontains'],
            'neighborhood': ['icontains'],
        }
