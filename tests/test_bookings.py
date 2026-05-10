import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from immogab.services import check_booking_overlap

def test_booking_no_overlap():
    # Booking 1: 10:00 to 12:00
    b1_start = datetime(2026, 5, 10, 10, 0)
    b1_end = datetime(2026, 5, 10, 12, 0)

    # New Booking: 12:00 to 14:00 (Starts exactly when b1 ends)
    new_start = datetime(2026, 5, 10, 12, 0)
    new_end = datetime(2026, 5, 10, 14, 0)

    existing_bookings = [
        MagicMock(start_time=b1_start, end_time=b1_end)
    ]

    # Should not overlap
    assert check_booking_overlap(new_start, new_end, existing_bookings) is False

def test_booking_overlap_detected():
    # Booking 1: 10:00 to 12:00
    b1_start = datetime(2026, 5, 10, 10, 0)
    b1_end = datetime(2026, 5, 10, 12, 0)

    # New Booking: 11:30 to 13:00 (Starts during b1)
    new_start = datetime(2026, 5, 10, 11, 30)
    new_end = datetime(2026, 5, 10, 13, 0)

    existing_bookings = [
        MagicMock(start_time=b1_start, end_time=b1_end)
    ]

    # Should overlap
    assert check_booking_overlap(new_start, new_end, existing_bookings) is True

def test_booking_overlap_inner():
    # Booking 1: 09:00 to 17:00
    b1_start = datetime(2026, 5, 10, 9, 0)
    b1_end = datetime(2026, 5, 10, 17, 0)

    # New Booking: 12:00 to 13:00 (Inside b1)
    new_start = datetime(2026, 5, 10, 12, 0)
    new_end = datetime(2026, 5, 10, 13, 0)

    existing_bookings = [
        MagicMock(start_time=b1_start, end_time=b1_end)
    ]

    assert check_booking_overlap(new_start, new_end, existing_bookings) is True
