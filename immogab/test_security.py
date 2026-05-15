import pytest
from django.conf import settings
from datetime import timedelta
from unittest import mock

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
    assert settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] == timedelta(minutes=15)
    assert settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] == timedelta(days=1)
    assert settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"] is True

def test_production_security_headers():
    """
    Test that security headers are correctly configured when DEBUG is False.
    Since we cannot easily reload settings during a test run if they are
    evaluated at module level, we check the values that should be set
    given that our test environment typically has DEBUG=False.
    """
    if not settings.DEBUG:
        assert settings.SECURE_BROWSER_XSS_FILTER is True
        assert settings.SECURE_CONTENT_TYPE_NOSNIFF is True
        assert settings.SECURE_HSTS_INCLUDE_SUBDOMAINS is True
        assert settings.SECURE_HSTS_PRELOAD is True
        assert settings.SECURE_HSTS_SECONDS == 31536000
        assert settings.SESSION_COOKIE_SECURE is True
        assert settings.CSRF_COOKIE_SECURE is True
        assert settings.X_FRAME_OPTIONS == "DENY"
