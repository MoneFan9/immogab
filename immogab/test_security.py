import pytest
from django.conf import settings
from django.test import override_settings
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
    assert settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] == timedelta(minutes=15)
    assert settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"] == timedelta(days=1)

@override_settings(DEBUG=False)
def test_production_security_settings_when_debug_false():
    # When DEBUG is False, these settings should be enabled
    # Note: These settings are defined at the module level in settings.py
    # based on the DEBUG value at import time.
    # To truly test the conditional logic in settings.py, we'd need to reload settings,
    # but here we check if they are correctly set in the environment.

    # Actually, settings.py logic for production security settings is:
    # if not DEBUG:
    #     SESSION_COOKIE_SECURE = True
    #     ...

    # If the test environment starts with DEBUG=True (default for many django test setups),
    # then at import time, these won't be set.

    # Let's check the current state (as imported)
    if not settings.DEBUG:
        assert settings.SESSION_COOKIE_SECURE is True
        assert settings.CSRF_COOKIE_SECURE is True
        assert settings.SECURE_HSTS_SECONDS == 31536000
        assert settings.SECURE_HSTS_INCLUDE_SUBDOMAINS is True
        assert settings.SECURE_HSTS_PRELOAD is True
