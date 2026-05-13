import os
import sys
import django
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'immogab.settings')
django.setup()

from immogab.services import (
    search_properties,
    validate_kyc,
    check_booking_overlap,
    MockPaymentGateway,
    call_jeedom_webhook
)

def run_simulation():
    print("--- Début de la simulation du parcours ImmoGab ---")

    # 1. Recherche d'une maison à Libreville
    print("\n1. Recherche d'une propriété à Libreville...")
    results = search_properties(query="Libreville", property_type="Maison")
    if not results:
        print("[-] AUCUNE PROPRIÉTÉ TROUVÉE.")
        return

    target = results[0]
    print(f"[+] Propriété trouvée : {target.title} à {target.location}")

    # 2. KYC
    print("\n2. Vérification KYC de l'utilisateur...")
    user = MagicMock()
    user.id_card_number = "GAB-2024-X99"
    user.is_kyc_verified = False

    try:
        validate_kyc(user)
        print(f"[+] KYC validé pour l'utilisateur. Statut : {user.is_kyc_verified}")
    except Exception as e:
        print(f"[-] ÉCHEC KYC : {e}")
        return

    # 3. Vérification des disponibilités (No overlap)
    print("\n3. Vérification de la disponibilité...")
    start = datetime.now() + timedelta(days=1)
    end = start + timedelta(hours=4)
    existing_bookings = [] # Mock empty list

    is_overlapping = check_booking_overlap(start, end, existing_bookings)
    if not is_overlapping:
        print(f"[+] Créneau disponible de {start} à {end}")
    else:
        print("[-] Créneau non disponible.")
        return

    # 4. Paiement Fictif
    print("\n4. Initialisation du paiement (Mock)...")
    gateway = MockPaymentGateway()
    payment = gateway.process_payment(amount=20000, currency="XAF", reference="E2E-SIM-001")
    if payment['status'] == 'success':
        print(f"[+] Paiement réussi ! ID Transaction : {payment['transaction_id']}")
    else:
        print("[-] Échec du paiement.")
        return

    # 5. Signal Jeedom
    print("\n5. Envoi du signal Jeedom (Mocké)...")
    # We need to patch requests.post because we don't have a real Jeedom box
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"jsonrpc": "2.0", "result": "success", "id": 1}

        try:
            success = call_jeedom_webhook(
                api_url="http://jeedom-gab.local/api",
                command="CMD_OPEN_LOCK_VILLA_1",
                api_key="SIMULATION_KEY_123"
            )
            if success:
                print("[+] Signal Jeedom envoyé avec succès ! La serrure est ouverte.")
            else:
                print("[-] Échec de l'envoi du signal Jeedom.")
        except Exception as e:
            print(f"[-] ERREUR LORS DE L'APPEL JEEDOM : {e}")

    print("\n--- Simulation terminée avec succès ---")

if __name__ == "__main__":
    run_simulation()
