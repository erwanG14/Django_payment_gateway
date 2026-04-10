from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def liste_objet(requests):
    return HttpResponse("salut voici la liste d'objet")
