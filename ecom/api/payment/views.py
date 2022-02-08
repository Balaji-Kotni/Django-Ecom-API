from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="yp6k39x8xqczc7r7",
        public_key="zx54jfkk2p7cbrqh",
        private_key="db553262abf3cc4463e9c54a2ca4b6c6"
    )
)


@login_required
def Validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def genrate_token(request, id, token):

    if not Validate_user_session(id, token):
        return JsonResponse({"error": "Invalid session, Please re-login!"})

    return JsonResponse({'clientToken': gateway.client_token.generate(), "success": True, "msg": "client token genrated succesfully"})


@csrf_exempt
def payment_process(request, id, token):

    if not Validate_user_session(id, token):
        return JsonResponse({"error": "Invalid session, Please re-login!"})
    if request.method == 'POST':

        nonce_from_the_client = request.POST['payment_method_nonce']
        amount = request.POST['amount']

        result = gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce_from_the_client,
            # TODO we need to do it

            # "device_data": device_data_from_the_client,
            "options": {
                "submit_for_settlement": True
            }
        })

        if result.is_success:
            return JsonResponse({
                "success": result.is_success,
                "transaction": {"id": result.transaction.id,
                                "amount": result.transaction.amount}
            })
        else:
            return JsonResponse({"error": True, "success": False, "msg": 'Transaction not successfull'})
    else:
        return JsonResponse({"error": "Please use POST method"})
