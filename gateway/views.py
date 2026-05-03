from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import requests

from .models import create_session,Client,Token,Transaction

# Create your views here.

def paiement(request):
    token = request.session.get('token')
    if request.method == "POST":
        banque = request.POST.get("banque")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        info_carte = request.POST.get("info_carte")
        prix = request.session.get('prix')
        token_objects,created = Token.objects.get_or_create(code = str(token))
        client,created = Client.objects.get_or_create(banque = banque, nom = nom, prenom = prenom, info_carte = info_carte, token = token_objects)
        transaction = Transaction.objects.create(banque = banque, info_carte = info_carte, token = token_objects,prix_transaction = prix)
        request.session["transaction_id"] = int(transaction.id)
        transaction_data = {
            "nom_client" : client.nom,
            "prenom_client" : client.prenom,
            "banque" : transaction.banque,
            "info_carte" : transaction.info_carte,
            "montant_transaction" : transaction.prix_transaction,
            "refus" : True,
        }
        
        print("salut gereur de meuf")
        print(reverse("reception_transaction"))
        reponse = transaction.send_transaction_to_banque("http://localhost:8000/"+str(reverse("reception_transaction")),transaction_data)
        print(reponse.text)
        data_recue = reponse.json()
        if data_recue["refus"] == True:
            return redirect(""+str(reverse("echec_paiement")))
        if data_recue["refus"] == False:
            return redirect(""+str(reverse("reussite_paiement")))
        
    if token:
        return render(request,"gateway/paiement.html")
        

def recevoir_transaction_marchand(request):
    nom = request.session.get('nom')
    prix = request.session.get('prix')
    session_marchand = create_session(nom = nom, prix = prix)

    request.session['token'] = str(session_marchand.token.code)

    return redirect('initier')
