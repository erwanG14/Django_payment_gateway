from .models import ClientBanque,CompteBancaire
from django.conf import settings

import json
import hmac
import hashlib
import time

from django.core.exceptions import PermissionDenied, ValidationError
def get_client_compte(data_client):
    try:
          client = ClientBanque.objects.get(
               nom = data_client["nom"],
               prenom = data_client["prenom"],
               numero_carte = data_client["numero_carte"],
          )

          compte = CompteBancaire.objects.get(
             client_banque = client,
          )
          return compte
    except ClientBanque.DoesNotExist:
         return False
    except CompteBancaire.DoesNotExist:
         return False
    


def verif_compte(data_client,data_transaction):
    compte = get_client_compte(data_client)
    if not compte:
        return {"refus" : True , "reason" : "no acccount"}
    else:
        if compte.solde - data_transaction["montant"] > 0 :

            if compte.client_banque.nom == data_transaction["nom"]:

                if compte.client_banque.prenom == data_transaction["prenom"]:

                    if compte.client_banque.numero_carte == data_transaction["numero_carte"]:
                        
                        return {"refus" : False}
                    
                
        return {"refus" : True}
    

    
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
        settings.BANQUE_SECRET.encode(),
        payload_to_sign,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected_signature):
        raise PermissionDenied("Signature invalide")