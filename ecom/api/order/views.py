from rest_framework import viewsets
from django.http import JsonResponse
from .serializer import OrderSerializer
from .models import Order
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def ValidateUserSession(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    if not ValidateUserSession(id, token):
        return JsonResponse({"error": "Please re-login", "code": "402"})

    if request.method == "POST":
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['transaction_id']
        products = request.POST['products']
        total_products = len(products.split(',')[:-1])
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({"error": "User Does Not Exist"})

        oder = Order(user=user, product_names=products, total_products=total_products,
                     transaction_id=transaction_id, total_amount=amount)
        oder.save()
        return JsonResponse({"success": True, "error": False, "msg": "order placed succesfully"})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderSerializer
