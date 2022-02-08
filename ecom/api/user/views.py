from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializer import CustomSerializer
from .models import CoustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import re
import random
import string
# Create your views here.


def genrate_session_token(length=10):
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=length))


@csrf_exempt
def signin(request):
    print(request.method)
    if not request.method == 'POST':
        return JsonResponse({"error": "send a post request with valid parameters"})
    username = request.POST['email']
    password = request.POST['password']
# validation Part
    if not re.match("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", username):
        return JsonResponse({"error": "please enter a valid email address"})

    if len(password) < 3:
        return JsonResponse({"error": "Password needs to be atlest of 3 charters"})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)

        if user.check_password(password):
            user_dict = UserModel.objects.filter(
                email=username).values().first()
            user_dict.pop('password')
            print(user.session_token)
            if user.session_token != '0':
                user.session_token = "0"
                user.save()
                return JsonResponse({"error": "previous session alredy exists!"})
            token = genrate_session_token(length=15)
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({"token": token, "user": user_dict})
        else:
            return JsonResponse({"error": "Invalid Password"})
    except UserModel.DoesNotExist:
        return JsonResponse({"error": "Invalid Email"})


@csrf_exempt
def signout(request):
    logout(request)
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({"error": "Invalid Id"})
    return JsonResponse({"success": "Logout successfully"})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {"create": [AllowAny]}

    queryset = CoustomUser.objects.all().order_by("id")
    serializer_class = CustomSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]
