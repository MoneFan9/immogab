import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from unittest.mock import MagicMock

# --- KYC and Booking Logic ---

def validate_kyc(user):
    """
    Validates that a user has provided an ID card number for KYC.
    Sets is_kyc_verified to True if valid.
    """
    id_card = getattr(user, 'id_card_number', None)
    if not id_card:
        raise ValueError("ID card is required for KYC")

    user.is_kyc_verified = True
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
    Mocks searching for properties.
    In a real app, this would query the Property model.
    """
    # Mock data
    mock_properties = [
        MagicMock(id=1, title="Villa Bord de Mer", location="Libreville", province="Estuaire", type="Maison"),
        MagicMock(id=2, title="Appartement Centre-Ville", location="Libreville", province="Estuaire", type="Appartement"),
        MagicMock(id=3, title="Terrain Sablière", location="Libreville", province="Estuaire", type="Terrain"),
        MagicMock(id=4, title="Espace Événementiel Port-Gentil", location="Port-Gentil", province="Ogooué-Maritime", type="Espace Événementiel"),
    ]

    results = []
    for prop in mock_properties:
        match = True
        if query and query.lower() not in prop.title.lower() and query.lower() not in prop.location.lower():
            match = False
        if province and prop.province != province:
            match = False
        if property_type and prop.type != property_type:
            match = False

        if match:
            results.append(prop)

    return results

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
