import pytest
from django.conf import settings
from datetime import timedelta

@pytest.mark.django_db
def test_debug_is_false_by_default():
    # We expect DEBUG to be False because we didn't set the env var in this test environment
    # and our logic defaults it to False.
    assert settings.DEBUG is False

def test_drf_authentication_classes():
    assert "rest_framework_simplejwt.authentication.JWTAuthentication" in settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]

def test_drf_permission_classes():
    assert "rest_framework.permissions.IsAuthenticated" in settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]

def test_cors_middleware_is_present():
    assert "corsheaders.middleware.CorsMiddleware" in settings.MIDDLEWARE
    # Ensure it's before CommonMiddleware
    cors_index = settings.MIDDLEWARE.index("corsheaders.middleware.CorsMiddleware")
    common_index = settings.MIDDLEWARE.index("django.middleware.common.CommonMiddleware")
    assert cors_index < common_index

def test_jwt_settings():
    # Requirement: 15 minutes
    assert settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] == timedelta(minutes=15)
    assert settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] == timedelta(days=1)

def test_secure_cookies():
    assert settings.SESSION_COOKIE_SECURE is True
    assert settings.CSRF_COOKIE_SECURE is True

def test_hsts_headers():
    assert settings.SECURE_HSTS_SECONDS == 31536000
    assert settings.SECURE_HSTS_INCLUDE_SUBDOMAINS is True
    assert settings.SECURE_HSTS_PRELOAD is True
