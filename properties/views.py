from rest_framework import viewsets, permissions, filters as drf_filters
from django_filters import rest_framework as filters
from .models import Property
from .serializers import PropertySerializer

class PropertyFilter(filters.FilterSet):
    min_price_hour = filters.NumberFilter(field_name="price_per_hour", lookup_expr='gte')
    max_price_hour = filters.NumberFilter(field_name="price_per_hour", lookup_expr='lte')
    min_price_day = filters.NumberFilter(field_name="price_per_day", lookup_expr='gte')
    max_price_day = filters.NumberFilter(field_name="price_per_day", lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['province', 'property_type', 'city', 'neighborhood']

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.AllowAny] # Allow search for everyone
    filterset_class = PropertyFilter
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    search_fields = ['title', 'description', 'city', 'neighborhood']
    ordering_fields = ['price_per_hour', 'price_per_day', 'created_at']
