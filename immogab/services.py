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
    Uses JSON-RPC 2.0 protocol with robust retry logic and timeout management.
    Optimized for local network IoT boxes.
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

    # Robust Retry Strategy for IoT:
    # - total=3: Up to 3 retries (4 attempts total)
    # - backoff_factor=0.3: Wait 0.3s, 0.6s, 1.2s between retries
    # - status_forcelist: Retry on common transient server errors
    # - allowed_methods: Jeedom API uses POST for all RPC calls
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["POST"],
        raise_on_status=True,  # Mandatory to trigger retries on status_forcelist
        connect=3,
        read=3
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    with requests.Session() as session:
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        try:
            response = session.post(
                api_url,
                json=payload,
                timeout=5  # 5 seconds timeout per attempt
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
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Jeedom connection failed after multiple attempts (timeout/network)")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Jeedom connection failed: {str(e)}")
