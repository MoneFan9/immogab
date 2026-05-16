import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from unittest.mock import MagicMock
from payments.interfaces import PaymentGateway as ModularPaymentGateway

# --- KYC and Booking Logic ---

def validate_kyc(user):
    """
    Validates that a user has provided an ID card number for KYC.
    Sets is_kyc_verified to True if valid.
    """
    if not hasattr(user, 'id_card_number') or not user.id_card_number:
        raise ValueError("ID card is required for KYC")

    user.is_kyc_verified = True
    # Save the user if it's a real model instance and not a MagicMock
    if hasattr(user, 'save') and not hasattr(user.save, 'assert_called'):
        user.save()
    return True

def check_booking_overlap(new_start, new_end, existing_bookings):
    """
    Checks if a new booking interval overlaps with any existing bookings.
    Intervals are [start, end).
    """
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

class ModularPaymentAdapter(PaymentGateway):
    """
    Adapts the new modular PaymentGateway to the legacy process_payment interface.
    """
    def __init__(self, provider_gateway: ModularPaymentGateway, phone_number: str):
        self.gateway = provider_gateway
        self.phone_number = phone_number

    def process_payment(self, amount, currency, reference):
        result = self.gateway.initiate_payment(amount, currency, self.phone_number, reference)
        return result

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
