import pytest
import requests
from unittest.mock import patch, MagicMock
from immogab.services import call_jeedom_webhook

@patch("requests.post")
def test_jeedom_webhook_success(mock_post):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
    mock_post.return_value = mock_response

    result = call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "secret_apikey")

    assert result is True
    mock_post.assert_called_once()

    # Verify JSON-RPC 2.0 format
    args, kwargs = mock_post.call_args
    sent_json = kwargs["json"]
    assert sent_json["jsonrpc"] == "2.0"
    assert sent_json["method"] == "cmd::exec"
    assert sent_json["params"]["apikey"] == "secret_apikey"
    assert sent_json["params"]["id"] == "lock_cmd"

@patch("requests.post")
def test_jeedom_webhook_rpc_error(mock_post):
    # Setup mock response with RPC error
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "jsonrpc": "2.0",
        "error": {"code": -32601, "message": "Method not found"},
        "id": 1
    }
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom RPC error: Method not found"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "secret_apikey")

@patch("requests.post")
def test_jeedom_webhook_401_unauthorized(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_post.return_value = mock_response

    with pytest.raises(PermissionError, match="Jeedom authentication failed"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "wrong_key")

@patch("requests.post")
def test_jeedom_webhook_500_server_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom server error"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.post")
def test_jeedom_webhook_timeout(mock_post):
    mock_post.side_effect = requests.exceptions.Timeout

    with pytest.raises(ConnectionError, match="Jeedom connection timed out"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.post")
def test_jeedom_webhook_other_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom error: 400"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.post")
def test_jeedom_webhook_request_exception(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException("Network fail")

    with pytest.raises(ConnectionError, match="Jeedom connection failed: Network fail"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.post")
def test_jeedom_webhook_malformed_json(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Simulate malformed JSON by making .json() raise an exception
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_post.return_value = mock_response

    with pytest.raises(ConnectionError, match="Jeedom connection failed: Invalid JSON"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

# --- Payment Webhook Tests ---

from immogab.services import MockPaymentGateway

def test_payment_webhook_success():
    gateway = MockPaymentGateway()
    payload = {
        "transaction_id": "TXN-123",
        "event": "payment.success",
        "amount": 5000
    }

    result = gateway.handle_webhook(payload, signature="valid_sig")

    assert result["status"] == "processed"
    assert result["transaction_id"] == "TXN-123"

def test_payment_webhook_invalid_signature():
    gateway = MockPaymentGateway()
    payload = {"transaction_id": "TXN-123"}

    with pytest.raises(PermissionError, match="Invalid webhook signature"):
        gateway.handle_webhook(payload, signature="invalid_sig")

def test_payment_webhook_missing_data():
    gateway = MockPaymentGateway()
    payload = {"event": "payment.success"} # Missing transaction_id

    with pytest.raises(ValueError, match="Missing transaction_id in payload"):
        gateway.handle_webhook(payload)
