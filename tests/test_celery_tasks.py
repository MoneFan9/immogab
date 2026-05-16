import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from immogab.services import schedule_booking_lock_commands

@pytest.fixture
def mock_booking():
    booking = MagicMock()
    booking.start_time = datetime(2026, 6, 1, 10, 0)
    booking.end_time = datetime(2026, 6, 1, 12, 0)

    booking.property = MagicMock()
    booking.property.jeedom_api_url = "http://jeedom.local/api"
    booking.property.jeedom_api_key = "secret_key"
    booking.property.unlock_command_id = "unlock_123"
    booking.property.lock_command_id = "lock_123"

    return booking

@patch("immogab.tasks.send_jeedom_command.apply_async")
def test_schedule_booking_lock_commands(mock_apply_async, mock_booking):
    # Mocking task objects returned by apply_async
    mock_unlock_task = MagicMock(id="unlock-uuid")
    mock_lock_task = MagicMock(id="lock-uuid")
    mock_apply_async.side_effect = [mock_unlock_task, mock_lock_task]

    result = schedule_booking_lock_commands(mock_booking)

    assert result["unlock_task_id"] == "unlock-uuid"
    assert result["lock_task_id"] == "lock-uuid"
    assert mock_apply_async.call_count == 2

    # Check Unlock call
    unlock_call = mock_apply_async.call_args_list[0]
    assert unlock_call.kwargs['args'] == [
        "http://jeedom.local/api",
        "unlock_123",
        "secret_key"
    ]
    assert unlock_call.kwargs['eta'] == mock_booking.start_time

    # Check Lock call
    lock_call = mock_apply_async.call_args_list[1]
    assert lock_call.kwargs['args'] == [
        "http://jeedom.local/api",
        "lock_123",
        "secret_key"
    ]
    assert lock_call.kwargs['eta'] == mock_booking.end_time

from immogab.services import confirm_booking

@patch("immogab.services.schedule_booking_lock_commands")
def test_confirm_booking_triggers_iot(mock_schedule, mock_booking):
    result = confirm_booking(mock_booking)

    assert result is True
    assert mock_booking.status == "CONFIRMED"
    mock_schedule.assert_called_once_with(mock_booking)
