from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse , Http404
from django.urls import reverse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from .service import verif_compte, parse_json_body,verify_gateway_signature
# Create your views here.

@csrf_exempt
def reception_transaction(request):
    verify_gateway_signature(request)
    data = parse_json_body(request)
    print("ici la banque")
    print(data)
    nom_requete = data["nom_client"]
    prenom_requete = data["prenom_client"]
    numero_carte = data["numero_carte"]
    montant = data["montant_transaction"]

    client_data = {
        "nom" : nom_requete,
        "prenom" : prenom_requete,
        "numero_carte" : numero_carte,
    }

    data_transaction = {
        "montant" : montant,
        "nom" : nom_requete,
        "prenom" : prenom_requete,
        "numero_carte" : numero_carte,
    }

    accord = verif_compte(client_data, data_transaction)
    accord = JsonResponse(accord)
    print("action_banque_fini")
    print(accord)
    return accord
