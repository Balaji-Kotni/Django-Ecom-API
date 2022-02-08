from rest_framework import viewsets
from .serializer import ProductSerializers
from .models import Product
# Create your views here.


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializers
