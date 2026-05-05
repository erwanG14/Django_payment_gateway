from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .service import verif_compte, parse_json_body, verify_gateway_signature

# Create your views here.


@csrf_exempt
def reception_transaction(request):

    verify_gateway_signature(request)
    data = parse_json_body(request)

    name_client = data["name_client"]
    surname_client = data["surname_client"]
    card_data = data["card_data"]
    price_transaction = data["price_transaction"]

    client_data = {
        "name": name_client,
        "surname": surname_client,
        "card_data": card_data,
    }

    data_transaction = {
        "price_transcation": price_transaction,
        "name": name_client,
        "surname": surname_client,
        "card_data": card_data,
    }

    accord = verif_compte(client_data, data_transaction)
    accord = JsonResponse(accord)
    return accord
