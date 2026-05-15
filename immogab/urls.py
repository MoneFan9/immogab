from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from properties.views import PropertyViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls")), # Basic DRF auth for browsable API
]
