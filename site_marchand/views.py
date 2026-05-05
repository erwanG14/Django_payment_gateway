from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from django.urls import reverse

from .models import Item
from .service import create_session,send_session_to_gateway
# Create your views here.

def catalogue(request):
    
    item = Item.objects.all()
    return render(request, "site_marchand/catalogue.html", {"produits" : item})

def initier(request):
    
    id_item =  request.GET.get('id')
    item = get_object_or_404(Item, id=id_item)
    
    if int(item.price) < 0:
        return HttpResponseBadRequest("price bellow 0")
    
    session = create_session(item = item)
    response = send_session_to_gateway(session)
    
    return redirect(response["payment_url"])

def reussite_paiement(request):

    context = {
        "transaction_id" : request.session.get('transaction_id'),
        "montant" : request.session.get('price'),
        "url" : "http://localhost:8000/" + str(reverse(catalogue)),
    }

    return render(request, "site_marchand/reussite_paiement.html", context)
    

def echec_paiement(request):
    context = {
        "raison" : "banq issue",
        "montant" : request.session.get('price'),
        "url" : "http://localhost:8000/" + str(reverse(catalogue)),
    }
    
    return render(request, "site_marchand/echec_paiement.html", context)

