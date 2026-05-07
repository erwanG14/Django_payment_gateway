from django.core.exceptions import PermissionDenied, ValidationError
from django.conf import settings

from .models import SessionMarchand
from .repo import create_client, create_card, create_transaction, get_session_marchande

import requests
import json
import hmac
import hashlib
import time


def sign_payload(body, timestamp):
    return hmac.new(
        settings.GATEWAY_BANQUE_SECRET.encode(),
        timestamp.encode() + b"." + body,
        hashlib.sha256,
    ).hexdigest()


def send_transaction_to_bank(transaction):
    transactionData = {
        "card_data": transaction.card.card_data,
        "name_client": transaction.card.client.name,
        "surname_client": transaction.card.client.surname,
        "price_transaction": transaction.price_transaction,
    }

    body = json.dumps(transactionData, separators=(",", ":")).encode()
    timestamp = str(int(time.time()))
    signature = sign_payload(body, timestamp)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "X-Idempotency-Key": str(transaction.idempotency_key),
    }

    response = requests.post(
        settings.BANQUE_SEND_TRANSACTION_URL,
        data=body,
        headers=headers,
    )

    return response.json()


def create_or_get_session(data):
    item_name = data["item_name"]
    price_transaction = data["amount"]
    idempotency_key = data["idempotency_key"]

    session, created = SessionMarchand.objects.get_or_create(
        item_name=item_name,
        price_transaction=price_transaction,
        idempotency_key=idempotency_key,
    )

    return session


def verify_merchant_signature(request):
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
        settings.MERCHANT_SECRET.encode(), payload_to_sign, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise PermissionDenied("Signature invalide")


def parse_json_body(request):
    try:
        return json.loads(request.body)

    except json.JSONDecodeError:
        raise ValidationError("JSON invalide")
    
def create_and_send_transaction_to_bank(bank,name,surname,url_code,card_data):
    client = create_client(
        bank=bank,
        name=name,
        surname=surname
    )
    card = create_card(
        card_data=card_data,
        client=client
    )
    session = get_session_marchande(
        url_code=url_code
    )
    return send_transaction_to_bank(
        create_transaction(
            bank=bank,
            price_transaction=session.price_transaction,
            card=card,
    ))



