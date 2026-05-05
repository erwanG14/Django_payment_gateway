from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError

from .models import ClientBank, BankAccount

import json
import hmac
import hashlib
import time


def get_client_compte(data_client):
    try:
        client = ClientBank.objects.get(
            name=data_client["name"],
            surname=data_client["surname"],
            card_data=data_client["card_data"],
        )

        compte = BankAccount.objects.get(
            client_bank=client,
        )
        return compte
    except ClientBank.DoesNotExist:
        return False
    except BankAccount.DoesNotExist:
        return False


def verif_compte(data_client, data_transaction):
    account = get_client_compte(data_client)
    if not account:
        return {"refus": True, "reason": "no acccount"}
    else:
        if account.balance - data_transaction["price_transcation"] > 0:

            if account.client_bank.name == data_transaction["name"]:

                if account.client_bank.surname == data_transaction["surname"]:

                    if account.client_bank.card_data == data_transaction["card_data"]:

                        return {"refus": False}

        return {"refus": True}


def parse_json_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        raise ValidationError("JSON invalide")


def verify_gateway_signature(request):
    timestamp = request.headers.get("X-Timestamp")
    signature = request.headers.get("X-Signature")

    if not timestamp or not signature:
        raise PermissionDenied("Signature manquante")

    try:
        timestamp_int = int(timestamp)
    except ValueError:
        raise PermissionDenied("Timestamp invalide")

    now = int(time.time())

    if abs(now - timestamp_int) > 300:
        raise PermissionDenied("Requête expirée")

    payload_to_sign = timestamp.encode() + b"." + request.body

    expected_signature = hmac.new(
        settings.BANQUE_SECRET.encode(), payload_to_sign, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise PermissionDenied("Signature invalide")
