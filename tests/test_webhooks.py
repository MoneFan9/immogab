import pytest
import requests
from unittest.mock import patch, MagicMock
from immogab.services import call_jeedom_webhook, get_jeedom_session

@pytest.fixture(autouse=True)
def reset_jeedom_session():
    """Reset the module-level session before each test."""
    from immogab import services
    services._jeedom_session = None

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

    # Verify timeout and headers
    assert kwargs["timeout"] == (3.05, 27)

    # Check session headers (User-Agent)
    session = get_jeedom_session()
    assert session.headers["User-Agent"] == "ImmoGab-IoT-Agent/1.0"

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
def test_jeedom_webhook_408_timeout_status(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 408
    mock_post.return_value = mock_response

    # urllib3 will retry on 408, so eventually it might raise RuntimeError (on 5th attempt)
    # or if we mock it to always return 408, it will raise the last response error
    with pytest.raises(RuntimeError, match="Jeedom error: 408"):
         call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "key")

@patch("requests.Session.post")
def test_jeedom_webhook_429_rate_limit(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_post.return_value = mock_response

    with pytest.raises(RuntimeError, match="Jeedom error: 429"):
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
    with patch("requests.Session.mount") as mock_mount:
        # We need to trigger session creation
        session = get_jeedom_session()

        # Check that mount was called for http and https
        mount_calls = {call.args[0]: call.args[1] for call in mock_mount.call_args_list}
        assert "http://" in mount_calls
        assert "https://" in mount_calls

        adapter = mount_calls["http://"]
        retry = adapter.max_retries
        assert retry.total == 5
        assert retry.backoff_factor == 1
        assert set([408, 429, 500, 502, 503, 504]).issubset(set(retry.status_forcelist))
        assert retry.raise_on_status is True
        assert adapter._pool_connections == 10
        assert adapter._pool_maxsize == 20
