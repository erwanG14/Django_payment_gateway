from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseBadRequest,request,HttpResponse
from django.template import loader
from django.urls import reverse
import requests

from .models import Objet
# Create your views here.

def catalogue(request):
    
    objet = Objet.objects.all()
    return render(request, "site_marchand/catalogue.html", {"produits" : objet})

def initier(request):

    token = request.session.get('token')
    if token:
        url = 'http://localhost:8000/gateway/paiement/'
        return redirect(url)
    
    id_objet =  request.GET.get('id')
    objet = get_object_or_404(Objet, id=id_objet)
    
    if int(objet.prix) < 0:
        return HttpResponseBadRequest("prix invalide")
    
    request.session['nom'] = str(objet.nom)
    request.session['prix'] = int(objet.prix)    
    
    return redirect('recevoir_transaction_marchand')

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

