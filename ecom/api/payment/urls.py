from django.urls import path, include
from . import views

urlpatterns = [
    path('gettoken/<str:id>/<str:token>/',
         views.genrate_token, name="Token.Genrate"),
    path('process/<str:id>/<str:token>/',
         views.payment_process, name="payment_process"),
]
