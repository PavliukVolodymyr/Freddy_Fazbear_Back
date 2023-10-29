from django.shortcuts import render


from rest_framework import viewsets
from .models import Dish,Customer
from .serializers import MyModelSerializer,CustomerSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = MyModelSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Create your views here.
