from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from .models import Property
from .serializers import PropertySerializer

class PropertyFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price_per_hour", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price_per_hour", lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['province', 'property_type', 'min_price', 'max_price']

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'city', 'address']
    ordering_fields = ['price_per_hour', 'created_at']
    permission_classes = [permissions.AllowAny] # Allow search for all
