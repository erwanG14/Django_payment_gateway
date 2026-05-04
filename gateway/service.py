from .models import SessionMarchand,Token
from django.core.exceptions import PermissionDenied, ValidationError
from django.conf import settings
import uuid
import requests

import json
import hmac
import hashlib
import time

def send_transaction_to_banque(transaction,url):
        
        transactionData = {
              "banque" : transaction.banque,
              "numero_carte" : transaction.carte.numero_carte,
              "nom_client" : transaction.carte.client.nom,
              "prenom_client" : transaction.carte.client.prenom,
              "montant_transaction" : transaction.prix_transaction
        }

        response = requests.post(url,json=transactionData)
        return response


def create_or_get_session(data):

      nom_objet = data["nom_objet"]
      prix_transaction = data["ammount"]
      idempotency_key = data["idempotency_key"]
      
      session,created =  SessionMarchand.objects.get_or_create(
            nom_objet=nom_objet,
            prix_transaction=prix_transaction,
            idempotency_key = idempotency_key
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
            settings.MERCHANT_SECRET.encode(),
            payload_to_sign,
            hashlib.sha256
      ).hexdigest()

      if not hmac.compare_digest(signature, expected_signature):
            raise PermissionDenied("Signature invalide")
      

def parse_json_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        raise ValidationError("JSON invalide")
    
