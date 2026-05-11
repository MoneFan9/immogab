from rest_framework import viewsets, permissions, pagination
from django_filters import rest_framework as filters
from .models import Property
from .serializers import PropertySerializer

class PropertyPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PropertyFilter(filters.FilterSet):
    min_price_hour = filters.NumberFilter(field_name="price_per_hour", lookup_expr='gte')
    max_price_hour = filters.NumberFilter(field_name="price_per_hour", lookup_expr='lte')
    min_price_day = filters.NumberFilter(field_name="price_per_day", lookup_expr='gte')
    max_price_day = filters.NumberFilter(field_name="price_per_day", lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['province', 'property_type', 'city']

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing property listings.
    Supports filtering by province, property_type, city, and price ranges.
    """
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PropertyFilter
    pagination_class = PropertyPagination
    permission_classes = [permissions.AllowAny] # Allow public search
