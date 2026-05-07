from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .service import process_gateway_call

# Create your views here.


@csrf_exempt
def reception_transaction(request):
    answer_verified = process_gateway_call(request=request)
    answer_to_send = JsonResponse(answer_verified)
    return answer_to_send
