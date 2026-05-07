from django.conf import settings
from django.http import HttpResponseBadRequest

from.repo import get_item_404,create_session

import json
import time
import hmac
import hashlib
import requests





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
    response =  response.json()
    response["payment_issue"] = None
    return response

     
def launch_gateway_call(id_item):
    item = get_item_404(id_item)

    if int(item.price) <= 0:
            return {"payment_issue" : "bad_request", "reason" : "price under 0"}
    session = create_session(item=item)
    
    return send_session_to_gateway(session)
