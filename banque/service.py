from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError

from .models import ClientBank, BankAccount
from .repo import get_client_compte

import json
import hmac
import hashlib
import time

def verif_compte(data):
    account = get_client_compte(
        name=data["name_client"],
        surname=data["surname_client"],
        card_data=data["card_data"]
    )
    if not account:
        return {"refus": True, "reason": "no acccount"}
    else:
        if account.balance - data["price_transaction"] > 0:

            if account.client_bank.name == data["name_client"]:

                if account.client_bank.surname == data["surname_client"]:

                    if account.client_bank.card_data == data["card_data"]:

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
    
def process_gateway_call(request):
    verify_gateway_signature(request)
    data = parse_json_body(request)
    return verif_compte(data)
