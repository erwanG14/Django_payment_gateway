from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.views import View

from .models import Item
from .service import launch_gateway_call

# Create your views here.

# merge en class get post

class CatalogueView(View):
    def get(self,request):
        items = Item.objects.all()
        return render(request, "site_marchand/catalogue.html", {"items": items})


    def post(self,request):
        id_item = request.POST.get("id")     
        response = launch_gateway_call(id_item)
        if response["payment_issue"] == "bad_request" :
            return HttpResponseBadRequest(response["reason"])
        else : 
            return redirect(response["payment_url"])


def reussite_paiement(request):
    context = {
        "transaction_id": request.session.get("transaction_id"),
        "montant": request.session.get("price"),
        "url": "http://localhost:8000/" + str(reverse("catalogue")),
    }

    return render(request, "site_marchand/reussite_paiement.html", context)


def echec_paiement(request):
    context = {
        "raison": "banq issue",
        "montant": request.session.get("price"),
        "url": "http://localhost:8000/" + str(reverse("catalogue")),
    }

    return render(request, "site_marchand/echec_paiement.html", context)
