import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from django.conf import settings
from immogab.services import (
    validate_kyc,
    check_booking_overlap,
    call_jeedom_webhook,
    search_properties,
    MockPaymentGateway
)

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id_card_number = "GAB-E2E-TEST"
    user.is_kyc_verified = False
    return user

@pytest.fixture
def mock_property():
    prop = MagicMock()
    prop.id = 101
    prop.title = "Villa de Test à Libreville"
    prop.location = "Libreville"
    prop.province = "Estuaire"
    prop.type = "Maison"
    return prop

class TestQACompliance:
    """
    Test suite to verify functional E2E journey and architectural compliance.
    """

    @patch("requests.post")
    def test_full_e2e_journey(self, mock_post, mock_user, mock_property):
        # 1. SEARCH
        results = search_properties(query="Libreville")
        assert len(results) > 0, "No properties found for Libreville"
        target = [p for p in results if p.location == "Libreville"][0]
        assert target.province == "Estuaire"

        # 2. KYC
        assert validate_kyc(mock_user) is True
        assert mock_user.is_kyc_verified is True

        # 3. BOOKING OVERLAP
        now = datetime.now()
        start = now + timedelta(days=1)
        end = start + timedelta(hours=2)
        assert check_booking_overlap(start, end, []) is False

        # 4. PAYMENT (Mock)
        gateway = MockPaymentGateway()
        res = gateway.process_payment(15000, "XAF", "QA-TEST-REF")
        assert res["status"] == "success"

        # 5. JEEDOM SIGNAL
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
        mock_post.return_value = mock_response

        jeedom_ok = call_jeedom_webhook("http://fake-jeedom.local", "lock_1", "key_123")
        assert jeedom_ok is True

        # Verify JSON-RPC 2.0 protocol
        _, kwargs = mock_post.call_args
        assert kwargs["json"]["jsonrpc"] == "2.0"
        assert kwargs["json"]["method"] == "cmd::exec"

    def test_database_compliance(self):
        """Verify that PostgreSQL is used as per README."""
        db_engine = settings.DATABASES['default']['ENGINE']
        assert "postgresql" in db_engine.lower(), f"PostgreSQL is mandatory. Found: {db_engine}"

    def test_docker_infrastructure_existence(self):
        """Verify that Docker infrastructure files exist."""
        base_dir = Path(settings.BASE_DIR)
        dockerfile_exists = (base_dir / "Dockerfile").exists()
        docker_compose_exists = (base_dir / "docker-compose.yml").exists()

        assert dockerfile_exists, "Dockerfile is missing but mandatory."
        assert docker_compose_exists, "docker-compose.yml is missing but mandatory."

    def test_no_magicmock_in_source(self):
        """Verify that MagicMock is NOT used in production code (services.py)."""
        services_path = Path(settings.BASE_DIR) / "immogab" / "services.py"
        with open(services_path, "r") as f:
            content = f.read()

        assert "MagicMock" not in content, "MagicMock found in immogab/services.py. Use real models/objects in production path."

    def test_modular_architecture_compliance(self):
        """Verify that logic is moved to modular apps (core, properties, etc)."""
        base_dir = Path(settings.BASE_DIR)
        core_exists = (base_dir / "core").is_dir()
        properties_exists = (base_dir / "properties").is_dir()
        payments_exists = (base_dir / "payments").is_dir()

        assert core_exists, "App 'core' is missing (Modular architecture requirement)."
        assert properties_exists, "App 'properties' is missing (Modular architecture requirement)."
        assert payments_exists, "App 'payments' is missing (Modular architecture requirement)."
