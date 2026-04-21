from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests

from .models import create_session

# Create your views here.
def paiement(request):
    return HttpResponse("salut voici la page de paiment")

def recevoir_transaction_marchand(request):
    nom = request.session.get('nom')
    prix = request.session.get('prix')
    session_marchand = create_session(nom = nom, prix = prix)

    request.session['token'] = str(session_marchand.token.code)

    return redirect('initier')