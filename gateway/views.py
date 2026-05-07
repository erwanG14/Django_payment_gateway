from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import SessionMarchand
from .service import (
    create_or_get_session,
    verify_merchant_signature,
    parse_json_body,
    create_and_send_transaction_to_bank
)

# Create your views here.


class PaiementView(View):
    def get(self, request, url_code, *args, **kwargs):
        sessionMarchand = get_object_or_404(SessionMarchand, url_code=url_code)

        if sessionMarchand.status != "pending":
            return redirect("echec_paiement")
        return render(request, "gateway/paiement.html")

    def post(self, request, url_code, *args, **kwargs):
        bank = request.POST.get("banque")
        name = request.POST.get("nom")
        surname = request.POST.get("prenom")
        card_data = request.POST.get("info_carte")
        
        reponse_from_bank = create_and_send_transaction_to_bank(
            bank=bank,
            name=name,
            surname=surname,
            url_code=url_code,
            card_data=card_data
        )
    
        if reponse_from_bank["refus"]:

            return redirect("echec_paiement")

        return redirect("reussite_paiement")


@csrf_exempt
@require_POST
def recevoir_transaction_marchand(request):
    verify_merchant_signature(request)
    data = parse_json_body(request)
    session_marchand = create_or_get_session(data)

    return JsonResponse(
        {
            "gateway_session_id": str(session_marchand.url_code),
            "payment_url": f"http://localhost:8000/gateway/paiement/{session_marchand.url_code}/",
            "status": session_marchand.status,
        }
    )
