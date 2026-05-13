import requests
import uuid
from datetime import datetime
from abc import ABC, abstractmethod

# --- Booking Logic ---

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
