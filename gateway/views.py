from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def paiement(requests):
    return HttpResponse("salut voici la page de paiment")
