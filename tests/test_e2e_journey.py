import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from immogab.services import (
    validate_kyc,
    check_booking_overlap,
    call_jeedom_webhook,
    search_properties,
    MockPaymentGateway,
    PropertyMock
)

class UserMock:
    def __init__(self, id_card_number=None, is_kyc_verified=False):
        self.id_card_number = id_card_number
        self.is_kyc_verified = is_kyc_verified

@pytest.fixture
def mock_user():
    return UserMock(id_card_number="123456789")

@pytest.fixture
def mock_property():
    return PropertyMock(
        id=1,
        title="Villa à Libreville",
        location="Libreville",
        province="Estuaire",
        type="Maison",
        hourly_rate=5000
    )

@patch("requests.post")
def test_e2e_journey_success(mock_post, mock_user, mock_property):
    """
    Simulation du parcours de bout en bout :
    recherche d'une maison à Libreville, paiement fictif, et signal Jeedom.
    """
    # 1. Recherche d'une maison à Libreville
    properties = search_properties(query="Libreville", property_type="Maison")
    assert len(properties) > 0
    assert any(p.location == "Libreville" for p in properties)

    target_property = [p for p in properties if p.location == "Libreville"][0]
    assert target_property.hourly_rate > 0

    # 2. Validation KYC (Obligatoire selon Loi 025/2021)
    assert validate_kyc(mock_user) is True
    assert mock_user.is_kyc_verified is True

    # 3. Vérification de chevauchement de réservation
    start_time = datetime(2026, 6, 1, 10, 0)
    end_time = datetime(2026, 6, 1, 14, 0)

    # Simulation de réservations existantes (pas de chevauchement)
    existing_bookings = [
        MagicMock(start_time=datetime(2026, 6, 1, 8, 0), end_time=datetime(2026, 6, 1, 9, 0)),
        MagicMock(start_time=datetime(2026, 6, 1, 15, 0), end_time=datetime(2026, 6, 1, 17, 0)),
    ]
    assert check_booking_overlap(start_time, end_time, existing_bookings) is False

    # 4. Paiement Fictif (Design Pattern Strategy)
    gateway = MockPaymentGateway()
    amount = target_property.hourly_rate * 4 # 4 hours
    payment_result = gateway.process_payment(amount=amount, currency="XAF", reference="BOOK-E2E-123")

    assert payment_result["status"] == "success"
    assert payment_result["amount"] == amount
    assert payment_result["currency"] == "XAF"
    assert "transaction_id" in payment_result

    # 5. Signal Jeedom (JSON-RPC 2.0)
    # Configuration du mock pour une réponse Jeedom réussie
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
    mock_post.return_value = mock_response

    api_url = "http://jeedom.local/api"
    api_key = "secret_jeedom_key"
    command = "cmd_open_lock_123"

    jeedom_result = call_jeedom_webhook(
        api_url=api_url,
        command=command,
        api_key=api_key
    )

    assert jeedom_result is True

    # Vérification stricte du protocole JSON-RPC 2.0
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == api_url

    sent_json = kwargs["json"]
    assert sent_json["jsonrpc"] == "2.0"
    assert sent_json["method"] == "cmd::exec"
    assert sent_json["params"]["apikey"] == api_key
    assert sent_json["params"]["id"] == command
    assert "id" in sent_json
