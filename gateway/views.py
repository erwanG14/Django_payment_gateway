from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import requests

from .models import Client,Token,Transaction,Carte
from .service import create_session,send_transaction_to_banque

# Create your views here.

def paiement(request):

    token = request.session.get('token')
    if request.method == "POST":

        banque = request.POST.get("banque")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        prix = request.session.get('prix')
        numero_carte = request.POST.get('info_carte')
       

        token_objects,created = Token.objects.get_or_create(code = str(token))
        client,created = Client.objects.get_or_create(
            banque = banque,
            nom = nom,
            prenom = prenom,
        )
        carte_client = Carte.objects.create(
            numero_carte = numero_carte,
            client = client
        )
        
        transaction = Transaction.objects.create(
            banque = banque,
            carte = carte_client,
            token = token_objects,
            prix_transaction = prix,
            )
        
        request.session["transaction_id"] = int(transaction.id)

        reponse = send_transaction_to_banque(
            transaction,
            "http://localhost:8000/" + str(reverse("reception_transaction")),
            )
        
        data_recue = reponse.json()
        print(data_recue)
        if data_recue["refus"] :
            #logique a rajouter raison du refus
            return redirect("" + str(reverse("echec_paiement")))
        
        return redirect("" + str(reverse("reussite_paiement")))
        
    if token:

        return render(request, "gateway/paiement.html")
        

def recevoir_transaction_marchand(request):

    nom = request.session.get('nom')
    prix = request.session.get('prix')
    session_marchand = create_session(
        nom=nom,
        prix=prix,
        )

    request.session['token'] = str(session_marchand.token.code)

    return redirect('initier')
