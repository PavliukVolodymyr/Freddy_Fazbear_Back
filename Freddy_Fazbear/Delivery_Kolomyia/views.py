from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Dish,Customer
from .serializers import DishSerializer,CustomerSerializer
from rest_framework.authtoken.models import Token

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@api_view(['POST'])
def Auth(request):
    # Отримайте дані з запиту
    data = request.data
    serializer=CustomerSerializer(data=data)
    # Отримайте інформацію для автентифікації з бази даних
    dbInfo = Customer.getAuthInfo()
    
    for item in dbInfo:
        if (data.get('email') == item['email'])and(data.get('password') == item['password']):
            user = Customer.objects.get(email=data['email'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'success','token': token.key})
    return Response({'message': 'fail'})

# Create your views here.
