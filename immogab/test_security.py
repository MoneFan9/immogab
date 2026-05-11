import pytest
from django.conf import settings
from datetime import timedelta

@pytest.mark.django_db
def test_security_settings():
    """
    Verify security-related settings.
    """
    # Check JWT token lifetime
    assert settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] == timedelta(minutes=15)

    # Check default auth and permissions
    assert settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] == (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
    assert settings.REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] == (
        "rest_framework.permissions.IsAuthenticated",
    )

def test_production_security_settings(settings):
    """
    Verify production security settings when DEBUG is False.
    """
    settings.DEBUG = False
    # Triggering the conditional logic in settings usually requires re-evaluation,
    # but since we are testing the result of that logic applied to 'settings' object:
    # Actually, we should check if they are set in the settings module.
    # Because immogab.settings already evaluated this logic.

    # We can mock DEBUG in the module or just check what's there.
    # In our case, we added 'if not DEBUG' in settings.py

    from immogab import settings as immogab_settings
    # If DEBUG was False during import, these should be True.
    # By default in our settings.py, DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    # So if DEBUG env var is not set, it is False.

    if not immogab_settings.DEBUG:
        assert immogab_settings.SESSION_COOKIE_SECURE is True
        assert immogab_settings.CSRF_COOKIE_SECURE is True
        assert immogab_settings.SECURE_HSTS_SECONDS == 31536000
