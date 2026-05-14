import pytest
import requests
from unittest.mock import patch, MagicMock
from immogab.services import call_jeedom_webhook

@patch("immogab.services.get_jeedom_session")
def test_jeedom_webhook_split_timeout_config(mock_get_session):
    mock_session = MagicMock()
    mock_get_session.return_value = mock_session

    mock_200 = MagicMock()
    mock_200.status_code = 200
    mock_200.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
    mock_session.post.return_value = mock_200

    call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "secret_apikey")

    # Verify split timeout: (connect, read)
    args, kwargs = mock_session.post.call_args
    assert kwargs["timeout"] == (3.05, 10)

def test_get_jeedom_session_config():
    from immogab.services import get_jeedom_session
    session = get_jeedom_session()
    adapter = session.get_adapter("http://")
    assert adapter.max_retries.total == 3
    assert adapter.max_retries.backoff_factor == 1
    assert 500 in adapter.max_retries.status_forcelist
    assert set(adapter.max_retries.allowed_methods) == set(["POST"])

def test_jeedom_webhook_uses_session_and_closes_it():
    with patch("immogab.services.get_jeedom_session") as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        mock_200 = MagicMock()
        mock_200.status_code = 200
        mock_200.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}
        mock_session.post.return_value = mock_200

        call_jeedom_webhook("http://jeedom.local/api", "lock_cmd", "secret_apikey")

        mock_get_session.assert_called_once()
        mock_session.post.assert_called_once()
        mock_session.close.assert_called_once()
