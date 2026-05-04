from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse , Http404
from django.urls import reverse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from .service import verif_compte 
# Create your views here.

@csrf_exempt
def reception_transaction(request):

    data = json.loads(request.body)
    print("ici la banque")
    print(data)
    nom_requete = data.get("nom_client")
    prenom_requete = data.get("prenom_client")
    numero_carte = data.get("numero_carte")
    montant = data.get("montant_transaction")

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
    
    return accord
