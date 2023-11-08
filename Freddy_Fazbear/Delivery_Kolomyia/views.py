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

@api_view(['POST'])
def get_customer_id_by_token(request):
    token = request.data.get('token')  # Припустимо, що токен передається як POST параметр 'token'
    print(token)
    if not token:
        return Response({'error': 'Токен не надано.'})

    try:
        customer_token = CustomerToken.objects.get(token=token)
    except CustomerToken.DoesNotExist:
        return Response({'error': 'Токен недійсний.'})
    user_id = customer_token.customer.id  # Отримуємо ідентифікатор користувача з моделі CustomerToken

    return Response({'user_id': user_id})

@api_view(['POST'])
def register_customer(request):
        try:
            data = request.data
            email = data['email']
            password = data['password']
            first_name = data['first_name']
            last_name = data['last_name']

            if Customer.objects.filter(email=email).exists():
                return Response({'error': 'email UNIQUE constraint failed'}, status=400)
            # Створення користувача
            customer = Customer.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=email,
            )
            return Response({'message': 'Користувач зареєстрований успішно.'})
        except Exception as e:
            return Response({'error': str(e)})