from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



from .models import Client,Token,Transaction,Carte,SessionMarchand
from .service import create_or_get_session,send_transaction_to_banque,verify_merchant_signature,parse_json_body

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
        
        
    def post(self, request, *args, **kwargs):

        banque = request.POST.get("banque")
        nom = request.POST.get("nom")
        prenom = request.POST.get("prenom")
        prix = request.session.get('prix')
        numero_carte = request.POST.get('info_carte')

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
            prix_transaction = prix,
        )
        
        reponse = send_transaction_to_banque(transaction)
        print("voici la reponse de la banque")
        print(reponse)
        
        # modif de l'appel a la banque -> signature hmac pour sécuriser

        print(reponse)
        if reponse["refus"] :
            #logique a rajouter raison du refus
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
