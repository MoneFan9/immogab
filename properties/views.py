from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property
from .serializers import PropertySerializer
from .filters import PropertyFilter

class PropertyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing property instances.
    Supports optimized search and filtering.
    """
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title', 'description', 'city', 'neighborhood']
    ordering_fields = ['price_per_day', 'price_per_hour', 'created_at']

    def get_queryset(self):
        # Performance: Pre-fetch or Select related if there were any ForeignKey/ManyToMany
        # For now, we ensure ordering is handled efficiently at the DB level
        return super().get_queryset()
