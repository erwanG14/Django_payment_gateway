from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



from .models import Client,Token,Transaction,Carte
from .service import create_or_get_session,send_transaction_to_banque,verify_merchant_signature,parse_json_body

# Create your views here.

class PaiementView(View):
    def get(self,request, * args, **kwargs):

        token = request.session.get('token')
        if token:

            return render(request, "gateway/paiement.html")
        return redirect("echec_paiement")
        
    def post(self, request, *args, **kwargs):

        token = request.session.get('token')
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

        carte_client,created = Carte.objects.get_or_create(
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
            return redirect("echec_paiement")
        
        return redirect("reussite_paiement")
  
@csrf_exempt
@require_POST
def recevoir_transaction_marchand(request):
    # get API
    #nom = request.session.get('nom')
    #prix = request.session.get('prix')
    # check indempotency key
    verify_merchant_signature(request)
    data = parse_json_body(request)
    
    session_marchand = create_or_get_session(data)

    return JsonResponse({
        "gateway_session_id": str(session_marchand.id),
        "payment_url": f"http://localhost:8000/gateway/paiement/{session_marchand.id}/",
        "status": session_marchand.status,
    })
