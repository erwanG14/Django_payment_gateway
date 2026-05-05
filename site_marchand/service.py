from django.conf import settings

from .models import Session

import json
import time
import hmac
import hashlib
import requests
import uuid


def create_session(item):

    session = Session.objects.create(
        item=item.name,
        amount=item.price,
        idempotency_key=uuid.uuid4(),
        session_status="pending",
    )

    return session


def sign_payload(body, timestamp):

    return hmac.new(
        settings.GATEWAY_SECRET.encode(),
        timestamp.encode() + b"." + body,
        hashlib.sha256,
    ).hexdigest()


def send_session_to_gateway(session):

    data_session = {
        "item_name": session.item,
        "amount": session.amount,
        "idempotency_key": str(session.idempotency_key),
        "session_status": session.session_status,
    }

    body = json.dumps(data_session, separators=(",", ":")).encode()
    timestamp = str(int(time.time()))
    signature = sign_payload(body, timestamp)

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
