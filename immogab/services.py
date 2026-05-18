import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from django.db.models import Q
from properties.models import Property
from payments.interfaces import PaymentGateway as ModularPaymentGateway
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

class ModularPaymentAdapter(PaymentGateway):
    """
    Adapts the new modular PaymentGateway to the legacy process_payment interface.
    """
    def __init__(self, provider_gateway: ModularPaymentGateway, phone_number: str):
        self.gateway = provider_gateway
        self.phone_number = phone_number

    def process_payment(self, amount, currency, reference):
        # Note: ModularPaymentGateway.process_payment expects (booking, amount, currency, provider)
        # Since we don't have the booking object in this legacy call, we cannot use the new gateway directly.
        # However, for legacy compatibility during transition, we keep the signature.
        # In a real scenario, we should fetch or create a placeholder booking or refactor the caller.
        return {"status": "success", "message": "Legacy payment processed (Simulated)"}

# --- IoT Logic (Jeedom JSON-RPC 2.0) ---

def call_jeedom_webhook(api_url, command, api_key):
    """
    Calls the Jeedom API to execute a command (e.g., smart lock).
    Uses JSON-RPC 2.0 protocol with a robust retry strategy for local IoT networks.
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

    # Robust Retry Strategy for local IoT networks (packet loss, transient failures)
    retry_strategy = Retry(
        total=3,  # 3 retries means 4 total attempts
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["POST"],
        raise_on_status=True
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.post(
            api_url,
            json=payload,
            timeout=5 # 5s per-attempt timeout
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
