import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from properties.models import Property
from django.db.models import Q

# --- KYC and Booking Logic ---

def validate_kyc(user):
    """
    Validates that a user has provided an ID card number for KYC.
    Sets is_kyc_verified to True if valid.
    """
    if not hasattr(user, 'id_card_number') or not user.id_card_number:
        raise ValueError("ID card is required for KYC")

    user.is_kyc_verified = True
    user.save()
    return True

def check_booking_overlap(new_start, new_end, property_id):
    """
    Checks if a new booking interval overlaps with any existing PAID bookings for a property.
    Intervals are [start, end).
    """
    from bookings.models import Booking
    overlapping_bookings = Booking.objects.filter(
        property_id=property_id,
        status='PAID',
        start_time__lt=new_end,
        end_time__gt=new_start
    )
    return overlapping_bookings.exists()

# --- Search Logic ---

def search_properties(query="", province=None, property_type=None):
    """
    Searches for properties in the database.
    """
    queryset = Property.objects.all()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )

    if province:
        queryset = queryset.filter(province=province)

    if property_type:
        queryset = queryset.filter(property_type=property_type)

    return list(queryset)

# --- Payment Logic (Strategy Pattern) ---

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference):
        pass

class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation that validates automatically.
    """
    def process_payment(self, amount, currency, reference):
        return {
            "status": "success",
            "transaction_id": str(uuid.uuid4()),
            "amount": amount,
            "currency": currency,
            "reference": reference,
            "timestamp": datetime.now().isoformat()
        }

# --- IoT Logic (Jeedom JSON-RPC 2.0) ---

def call_jeedom_webhook(api_url, command, api_key):
    """
    Calls the Jeedom API to execute a command (e.g., smart lock).
    Uses JSON-RPC 2.0 protocol.
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

    try:
        response = requests.post(
            api_url,
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            # Additional check for JSON-RPC error in 200 response
            data = response.json()
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
