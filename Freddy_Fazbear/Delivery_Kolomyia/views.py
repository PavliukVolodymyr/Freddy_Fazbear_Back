from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Dish,Customer
from .serializers import DishSerializer,CustomerSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

@api_view(['POST'])
def Auth(request):
    data = request.data
    serializer = CustomerSerializer(data=data)
    
    # if serializer.is_valid():
    email = data.get('email')
    password = data.get('password')
        
    dbInfo = Customer.getAuthInfo()
    for item in dbInfo:
        if email == item['email'] and password == item['password']:
            # user = Customer.objects.get(email=email)
            user = get_user_model().objects.get(email=email)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'success', 'token': token.key})
    
    return Response({'message': 'fail'})
