from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Objet
# Create your views here.

def catalogue(requests):
    objet = Objet.objects.all()
    template = loader.get_template("site_marchand/catalogue.html")
    return render(requests,"site_marchand/catalogue.html",{"produits" : objet})
