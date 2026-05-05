from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseBadRequest,request,HttpResponse,Http404
from django.template import loader
from django.urls import reverse
import requests

from .models import Objet
from .service import create_session,send_session_to_gateway
# Create your views here.

def catalogue(request):
    
    objet = Objet.objects.all()
    return render(request, "site_marchand/catalogue.html", {"produits" : objet})

def initier(request):
    
    id_objet =  request.GET.get('id')
    objet = get_object_or_404(Objet, id=id_objet)
    
    if int(objet.prix) < 0:
        return HttpResponseBadRequest("prix invalide")
    
    session = create_session(produit = objet)
    reponse = send_session_to_gateway(session)
    
    return redirect(reponse["payment_url"])

def reussite_paiement(request):

    context = {
        "transaction_id" : request.session.get('transaction_id'),
        "montant" : request.session.get('prix'),
        "url" : "http://localhost:8000/" + str(reverse(catalogue)),
    }

    return render(request, "site_marchand/reussite_paiement.html", context)
    

def echec_paiement(request):
    context = {
        "raison" : "probleme bancaire",
        "montant" : request.session.get('prix'),
        "url" : "http://localhost:8000/" + str(reverse(catalogue)),
    }
    
    return render(request, "site_marchand/echec_paiement.html", context)

