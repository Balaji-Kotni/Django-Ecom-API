from rest_framework import routers
from . import views
from django.urls import path, include

routes = routers.DefaultRouter()
routes.register(r'', views.UserViewSet)

urlpatterns = [
    path('login/', views.signin, name='signin'),
    path('logout/<int:id>/', views.logout, name="signout"),
    path('', include(routes.urls))
]
