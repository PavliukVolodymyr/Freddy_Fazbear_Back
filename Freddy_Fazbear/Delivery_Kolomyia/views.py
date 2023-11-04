from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Dish,Customer,Restaurant,CustomerToken
from .serializers import DishSerializer,CustomerSerializer,RestaurantSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import secrets

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
def generate_customer_token(customer):
    CustomerToken.objects.filter(customer=customer).delete()
    token, created = CustomerToken.objects.get_or_create(customer=customer)
    if created:
        # Генеруємо токен для нового користувача
        token.token = secrets.token_urlsafe(30)
        token.save()
    return token.token
    

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
            customer = Customer.objects.get(email=email)
            # user = get_user_model().objects.get(username=username)
            # print(user)
            customer_token = generate_customer_token(customer)
            print(customer_token)
            return Response({'message': 'success', 'token': customer_token})
            # token, created = Token.objects.get_or_create(user=customer)
            # return Response({'message': 'success', 'token': token.key})
    
    return Response({'message': 'fail'})
