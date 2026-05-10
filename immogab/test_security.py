from django.test import TestCase
from django.conf import settings
import os

class SecuritySettingsTest(TestCase):
    def test_debug_is_false_by_default(self):
        # We expect DEBUG to be False because we didn't set the env var in this test environment
        # and our logic defaults it to False.
        self.assertFalse(settings.DEBUG)

    def test_drf_authentication_classes(self):
        self.assertIn(
            "rest_framework_simplejwt.authentication.JWTAuthentication",
            settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"]
        )

    def test_drf_permission_classes(self):
        self.assertIn(
            "rest_framework.permissions.IsAuthenticated",
            settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"]
        )

    def test_cors_middleware_is_present(self):
        self.assertIn("corsheaders.middleware.CorsMiddleware", settings.MIDDLEWARE)
        # Ensure it's before CommonMiddleware
        cors_index = settings.MIDDLEWARE.index("corsheaders.middleware.CorsMiddleware")
        common_index = settings.MIDDLEWARE.index("django.middleware.common.CommonMiddleware")
        self.assertLess(cors_index, common_index)

    def test_jwt_settings(self):
        from datetime import timedelta
        self.assertEqual(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"], timedelta(minutes=60))
        self.assertEqual(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"], timedelta(days=1))
