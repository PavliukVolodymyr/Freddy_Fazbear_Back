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
from django.contrib.auth import authenticate

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
    try:
        # Спробуйте отримати запис CustomerToken за допомогою токену
        customer_token = CustomerToken.objects.get(customer=customer)
        return customer_token.token
    except CustomerToken.DoesNotExist:
        # Якщо запис не знайдено, створіть новий токен
        new_token = secrets.token_urlsafe(30)
        CustomerToken.objects.create(customer=customer, token=new_token)
        return new_token
    

def Auth(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    try:
        # Отримати користувача за email
        customer = Customer.objects.get(email=email)
        print(customer)

        # Перевірити, чи пароль співпадає з хешем у базі даних
        passwords_match = customer.check_password(password)

        if passwords_match:
            customer_token = generate_customer_token(customer)
            return Response({'message': 'success', 'token': customer_token})
        else:
            return Response({'message': 'fail'})
    except Customer.DoesNotExist:
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
            customer_token = generate_customer_token(customer)
            return Response({'message': 'success', 'token': customer_token})
            
        except Exception as e:
            return Response({'error': str(e)})