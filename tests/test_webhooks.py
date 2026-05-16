import pytest
import requests
from unittest.mock import patch, MagicMock
from immogab.services import call_jeedom_webhook

@patch("requests.Session.post")
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

@patch("requests.Session.post")
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

@patch("requests.Session.post")
def test_jeedom_webhook_401_unauthorized(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_post.return_value = mock_response

    with pytest.raises(PermissionError, match="Jeedom authentication failed"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "wrong_key")

@patch("requests.Session.post")
def test_jeedom_webhook_500_server_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom server error"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.Session.post")
def test_jeedom_webhook_timeout(mock_post):
    mock_post.side_effect = requests.exceptions.Timeout

    with pytest.raises(ConnectionError, match="Jeedom connection timed out"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.Session.post")
def test_jeedom_webhook_other_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom error: 400"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.Session.post")
def test_jeedom_webhook_request_exception(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException("Network fail")

    with pytest.raises(ConnectionError, match="Jeedom connection failed: Network fail"):
        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

def test_verify_retry_config():
    """
    Verify that the session is correctly configured with retries.
    """
    with patch("requests.Session.mount") as mock_mount, \
         patch("requests.Session.post") as mock_post:

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
        mock_post.return_value = mock_response

        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

        # Check that mount was called for http and https
        mount_calls = {call.args[0]: call.args[1] for call in mock_mount.call_args_list}
        assert "http://" in mount_calls
        assert "https://" in mount_calls

        adapter = mount_calls["http://"]
        retry = adapter.max_retries
        assert retry.total == 3
        assert retry.backoff_factor == 0.3
        assert set([500, 502, 503, 504]).issubset(set(retry.status_forcelist))
        assert retry.raise_on_status is True
