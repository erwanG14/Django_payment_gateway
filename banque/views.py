from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
import json
from .models import Client_banque,compte_bancaire
# Create your views here.

def reception_transaction(request):
    data = json.load(request.body)
    nom_requete = data.get("nom_client")
    prenom_requete = data.get("prenom_client")
    info_carte = data.get("info_carte")
    montant = data.get("montant_transaction")
    client = get_object_or_404(Client_banque,nom = nom_requete, prenom = prenom_requete, info_bancaire = info_carte)
    compte = get_object_or_404(compte_bancaire,Client_banque = client)
    data_verif = {
        "nom" : nom_requete,
        "prenom" : prenom_requete,
        "info_bancaire" : info_carte,
    }
    accord = compte.verif_compte(data_verif)
    return HttpResponse(str(accord))
