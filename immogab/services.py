import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from unittest.mock import MagicMock
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --- KYC and Booking Logic ---

def validate_kyc(user):
    """
    Validates that a user has provided an ID card number for KYC.
    Sets is_kyc_verified to True if valid.
    """
    if not hasattr(user, 'id_card_number') or not user.id_card_number:
        raise ValueError("ID card is required for KYC")

    user.is_kyc_verified = True
    if hasattr(user, 'save'):
        user.save()
    return True

def check_booking_overlap(new_start, new_end, existing_bookings):
    """
    Checks if a new booking interval overlaps with any existing bookings.
    Intervals are [start, end).
    """
    if new_start >= new_end:
        raise ValueError("Start time must be before end time")

    for booking in existing_bookings:
        # Overlap if: (StartA < EndB) and (EndA > StartB)
        if new_start < booking.end_time and new_end > booking.start_time:
            return True
    return False

# --- Search Logic ---

def search_properties(query="", province=None, property_type=None):
    """
    Searches for properties using the real Property model.
    """
    from properties.models import Property
    from django.db.models import Q
    queryset = Property.objects.all()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(city__icontains=query) |
            Q(neighborhood__icontains=query)
        )

    if province:
        queryset = queryset.filter(province=province)

    if property_type:
        queryset = queryset.filter(property_type=property_type)

    return list(queryset)

# --- Payment Logic (Legacy support and Adapter) ---

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference):
        pass

class MockPaymentGateway(PaymentGateway):
    """
    DEPRECATED: Use payments.services.MockPaymentGateway instead.
    Mock implementation that validates automatically.
    """
    def process_payment(self, amount, currency, reference):
        from payments.services import MockPaymentGateway as NewMockGateway
        from bookings.models import Booking
        from properties.models import Property
        from django.contrib.auth import get_user_model
        from django.utils import timezone
        User = get_user_model()

        # Backward compatibility layer for old tests
        user, _ = User.objects.get_or_create(id=1, defaults={'username': 'legacy_user'})
        prop, _ = Property.objects.get_or_create(id=1, defaults={'title': 'Legacy Property', 'price_per_day': 100})

        booking, _ = Booking.objects.get_or_create(
            id=999, # Dummy ID for legacy support
            defaults={
                'user': user,
                'property': prop,
                'start_time': timezone.now(),
                'end_time': timezone.now(),
                'total_price': amount
            }
        )
        new_gateway = NewMockGateway()
        return new_gateway.process_payment(booking, amount, currency, "Legacy Provider")

class ModularPaymentAdapter(PaymentGateway):
    """
    Adapts the new modular PaymentGateway to the legacy process_payment interface.
    """
    def __init__(self, provider_gateway, phone_number: str):
        self.gateway = provider_gateway
        self.phone_number = phone_number

    def process_payment(self, amount, currency, reference):
        result = self.gateway.initiate_payment(amount, currency, self.phone_number, reference)
        return result

# --- IoT Logic (Jeedom JSON-RPC 2.0) ---

# Module-level session for connection pooling
_jeedom_session = None

def get_jeedom_session():
    """
    Returns a configured requests session for Jeedom API calls.
    Optimized for local IoT networks with connection pooling and robust retries.
    """
    global _jeedom_session
    if _jeedom_session is None:
        _jeedom_session = requests.Session()
        # Robust Retry Strategy for local IoT networks (packet loss, transient failures, rate limits)
        retry_strategy = Retry(
            total=5,  # Increased to 5 retries for better resilience
            backoff_factor=1,  # Exponential backoff: 1s, 2s, 4s, 8s, 16s
            status_forcelist=[408, 429, 500, 502, 503, 504],
            allowed_methods=["POST"],
            raise_on_status=True
        )
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        _jeedom_session.mount("http://", adapter)
        _jeedom_session.mount("https://", adapter)
        _jeedom_session.headers.update({"User-Agent": "ImmoGab-IoT-Agent/1.0"})
    return _jeedom_session

def call_jeedom_webhook(api_url, command, api_key):
    """
    Calls the Jeedom API to execute a command (e.g., smart lock).
    Uses JSON-RPC 2.0 protocol with an optimized session for local IoT networks.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "cmd::exec",
        "params": {
            "apikey": api_key,
            "id": command
        },
        "id": 1
    }

    session = get_jeedom_session()

    try:
        # Optimization: use (connect, read) timeout tuple.
        # 3.05s to connect (slightly more than a TCP packet retransmission window)
        # 27s to read (enough for local IoT response)
        response = session.post(
            api_url,
            json=payload,
            timeout=(3.05, 27)
        )

        if response.status_code == 200:
            # Additional check for JSON-RPC error in 200 response
            try:
                data = response.json()
            except ValueError:
                raise ConnectionError("Jeedom returned an invalid JSON response")

            if "error" in data:
                raise RuntimeError(f"Jeedom RPC error: {data['error'].get('message', 'Unknown error')}")
            return True
        elif response.status_code == 401:
            raise PermissionError("Jeedom authentication failed")
        elif response.status_code >= 500:
            raise RuntimeError("Jeedom server error")
        else:
            raise RuntimeError(f"Jeedom error: {response.status_code}")

    except requests.exceptions.Timeout:
        raise ConnectionError("Jeedom connection timed out")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Jeedom connection failed: {str(e)}")

# --- Booking-IoT Integration ---

def schedule_booking_lock_commands(booking):
    """
    Schedules 'Unlock' at the start of the booking and 'Lock' at the end.
    Expects booking to have:
    - start_time, end_time (datetime)
    - property with jeedom_api_url, jeedom_api_key, unlock_command_id, lock_command_id
    Returns a dict containing the task IDs for potential revocation.
    """
    from .tasks import send_jeedom_command

    # 1. Schedule UNLOCK
    unlock_task = send_jeedom_command.apply_async(
        args=[
            booking.property.jeedom_api_url,
            booking.property.unlock_command_id,
            booking.property.jeedom_api_key
        ],
        eta=booking.start_time
    )

    # 2. Schedule LOCK
    lock_task = send_jeedom_command.apply_async(
        args=[
            booking.property.jeedom_api_url,
            booking.property.lock_command_id,
            booking.property.jeedom_api_key
        ],
        eta=booking.end_time
    )

    return {
        "unlock_task_id": unlock_task.id,
        "lock_task_id": lock_task.id
    }

def confirm_booking(booking):
    """
    Confirms a booking and triggers the IoT lock scheduling.
    In a real app, this would also update the booking status in the DB.
    """
    booking.status = "CONFIRMED"

    # Trigger IoT scheduling
    schedule_booking_lock_commands(booking)

    return True
