from rest_framework import routers
from . import views
from django.urls import path, include

routes = routers.DefaultRouter()
routes.register(r'', views.ProductViewset)

urlpatterns = [
    path('', include(routes.urls))
]
