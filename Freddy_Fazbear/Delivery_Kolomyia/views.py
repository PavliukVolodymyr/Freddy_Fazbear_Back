from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Dish,Customer,Restaurant,CustomerToken,CartItem
from .serializers import DishSerializer,CustomerSerializer,RestaurantSerializer,CartItemSerializer
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

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
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
    
@api_view(['POST'])
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
        
@api_view(['POST'])
def add_dish_to_cart(request):
    customer_id = request.data.get('customer_id')
    dish_id = request.data.get('dish_id')

    try:
        customer = Customer.objects.get(id=customer_id)
        dish = Dish.objects.get(id=dish_id)
        cart_item, created = CartItem.objects.get_or_create(customer=customer, dish=dish)
        cart_item.quantity +=1
        cart_item.save()
        serializer = CustomerSerializer(customer)
        return Response({'message': 'success'})
    except Customer.DoesNotExist:
        return Response("Customer not found")
    except Dish.DoesNotExist:
        return Response("Dish not found")
    
@api_view(['POST'])
def change_count_in_cart(request):
    customer_id = request.data.get('customer_id')
    dish_id = request.data.get('dish_id')
    quantity = request.data.get('quantity', 1)
    try:
        cart_item = CartItem.objects.get(customer=customer_id, dish=dish_id)
        cart_item.quantity = quantity
        cart_item.save()
        serializer = CustomerSerializer(cart_item)
        return Response({'message': 'success'})
    except CartItem.DoesNotExist:
        return Response("CartItem not found")
    
@api_view(['POST'])
def delete_cart_item(request):
    cart_item_id=request.data.get('cart_item_id')
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart_item.delete()
        return Response({'message': 'success'})
    except CartItem.DoesNotExist:
        return Response("CartItem not found")
    