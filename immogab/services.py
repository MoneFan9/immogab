import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- KYC and Booking Logic ---

def validate_kyc(user):
    """
    Validates that a user has provided an ID card number for KYC.
    Sets is_kyc_verified to True if valid.
    """
    id_card = getattr(user, 'id_card_number', None)
    if not id_card or not str(id_card).strip():
        raise ValueError("ID card is required for KYC")

    user.is_kyc_verified = True
    return True

def check_booking_overlap(new_start, new_end, existing_bookings):
    """
    Checks if a new booking interval overlaps with any existing bookings.
    Intervals are [start, end).
    """
    for booking in existing_bookings:
        # Ensure booking has required attributes
        start = getattr(booking, 'start_time', None)
        end = getattr(booking, 'end_time', None)

        if start is None or end is None:
            continue

        # Overlap if: (StartA < EndB) and (EndA > StartB)
        if new_start < end and new_end > start:
            return True
    return False

# --- Search Logic ---

@dataclass
class PropertyMock:
    """
    Simple mock class to replace MagicMock in production-like logic.
    """
    id: int
    title: str
    location: str
    province: str
    type: str

def search_properties(query="", province=None, property_type=None):
    """
    Mocks searching for properties.
    In a real app, this would query the Property model.
    """
    # Mock data using typed dataclass instead of MagicMock
    mock_properties = [
        PropertyMock(id=1, title="Villa Bord de Mer", location="Libreville", province="Estuaire", type="Maison"),
        PropertyMock(id=2, title="Appartement Centre-Ville", location="Libreville", province="Estuaire", type="Appartement"),
        PropertyMock(id=3, title="Terrain Sablière", location="Libreville", province="Estuaire", type="Terrain"),
        PropertyMock(id=4, title="Espace Événementiel Port-Gentil", location="Port-Gentil", province="Ogooué-Maritime", type="Espace Événementiel"),
    ]

    results = []
    for prop in mock_properties:
        match = True

        # Robust attribute access
        title = getattr(prop, 'title', "")
        location = getattr(prop, 'location', "")
        p_province = getattr(prop, 'province', None)
        p_type = getattr(prop, 'type', None)

        if query:
            q = query.lower()
            if q not in title.lower() and q not in location.lower():
                match = False

        if province and p_province != province:
            match = False

        if property_type and p_type != property_type:
            match = False

        if match:
            results.append(prop)

    return results

# --- Payment Logic (Strategy Pattern) ---

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount, currency, reference):
        pass

    @abstractmethod
    def handle_webhook(self, payload, signature=None):
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

    def handle_webhook(self, payload, signature=None):
        """
        Simulates handling a payment webhook (e.g. from Airtel Money).
        """
        if signature == "invalid_sig":
            raise PermissionError("Invalid webhook signature")

        transaction_id = payload.get("transaction_id")
        if not transaction_id:
            raise ValueError("Missing transaction_id in payload")

        # Simulate business logic: update booking status
        return {
            "status": "processed",
            "transaction_id": transaction_id,
            "event": payload.get("event", "payment.success")
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
            try:
                data = response.json()
            except ValueError as e:
                raise ConnectionError(f"Jeedom connection failed: {str(e)}")
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
