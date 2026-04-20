from django.shortcuts import render
from django.http import HttpResponse,request
from django.template import loader

from .models import Objet
# Create your views here.

def catalogue(request):
    objet = Objet.objects.all()
    return render(request,"site_marchand/catalogue.html",{"produits" : objet})

def initier(request):
    id_objet =  request.GET.get('id')
    objet = Objet.objects.get(id= id_objet)
    nom = objet.nom
    prix = objet.prix
    return HttpResponse("voici la page initier pour l'objet "+nom)

