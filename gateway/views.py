from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Client,Transaction,Card,SessionMarchand
from .service import create_or_get_session, send_transaction_to_banque, verify_merchant_signature, parse_json_body

# Create your views here.

class PaiementView(View):
    def get(self,request, code_url, *args, **kwargs):
        
        sessionMarchand = get_object_or_404(
            SessionMarchand,
            code_url = code_url
        )

        if sessionMarchand.status != "pending":
            return redirect("echec_paiement")
        return render(request,"gateway/paiement.html")
        
        
    def post(self, request,code_url, *args, **kwargs):

        bank = request.POST.get("banque")
        name = request.POST.get("nom")
        surname = request.POST.get("prenom")
        session_marchand = SessionMarchand.objects.get(code_url = code_url)
        card_data = request.POST.get('info_carte')

        client,created = Client.objects.get_or_create(
            bank = bank,
            name = name,
            surname = surname,
        )

        card_client,created = Card.objects.get_or_create(
            card_data = card_data,
            client = client
        )

        transaction = Transaction.objects.create(
            bank = bank,
            card = card_client,
            price_transaction = session_marchand.price_transaction,
        )
        
        reponse = send_transaction_to_banque(transaction)
        if reponse["refus"] :

            return redirect("echec_paiement")
        
        return redirect("reussite_paiement")
  
@csrf_exempt
@require_POST
def recevoir_transaction_marchand(request):

    verify_merchant_signature(request)
    data = parse_json_body(request)
    session_marchand = create_or_get_session(data)

    return JsonResponse({
        "gateway_session_id": str(session_marchand.code_url),
        "payment_url": f"http://localhost:8000/gateway/paiement/{session_marchand.code_url}/",
        "status": session_marchand.status,
    })
