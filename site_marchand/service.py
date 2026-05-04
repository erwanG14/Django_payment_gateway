
import json
import time
import hmac
import hashlib
import requests
import uuid

from django.conf import settings
from .models import Session


def create_session(produit):
    session = Session.objects.create(
        objet=produit.nom,
        ammount=produit.prix,
        idempotency_key=uuid.uuid4(),
        session_status="pending",
    )
    return session

def sign_payload(body, timestamp):
    return hmac.new(
        settings.GATEWAY_SECRET.encode(),
        timestamp.encode() + b"." + body,
        hashlib.sha256
    ).hexdigest()

def send_session_to_gateway(session):

    data_session = {
        "nom_objet" : session.objet,
        "ammount" : session.ammount,
        "idempotency_key" : str(session.idempotency_key),
        "session_status" : session.session_status,
    }

    body = json.dumps(data_session, separators=(",", ":")).encode()
    timestamp = str(int(time.time()))
    signature = sign_payload(body,timestamp)

    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": timestamp,
        "X-Signature": signature,
        "X-Idempotency-Key": str(session.idempotency_key),
    }

    response = requests.post(
        settings.GATEWAY_CREATE_SESSION_URL,
        data=body,
        headers=headers,
    )
    if not response.ok:
        print(response.status_code)
        print(response.text)
        response.raise_for_status()
    return response.json()
