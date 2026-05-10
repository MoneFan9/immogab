import pytest
import requests
from unittest.mock import patch, MagicMock
from immogab.services import call_jeedom_webhook

@patch("requests.post")
def test_jeedom_webhook_success(mock_post):
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    result = call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "secret_apikey")

    assert result is True
    mock_post.assert_called_once()

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
