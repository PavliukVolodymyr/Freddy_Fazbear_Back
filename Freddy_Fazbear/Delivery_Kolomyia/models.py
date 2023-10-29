from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

class Admin(AbstractUser):
    admin_id = models.IntegerField() 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group, related_name="admin_users")
    user_permissions = models.ManyToManyField(Permission, related_name="admin_permissions")
    
class Dish(models.Model):
    restaurant_id = models.IntegerField()
    name = models.CharField(max_length=30,default='Default Name')  
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    
class Restaurant(models.Model):
    name = models.CharField(max_length=30, default='Default Name')
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3,decimal_places=2)
    photo = models.ImageField(upload_to='restaurant_photos/' , default='default.jpg')
    
class Customer(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    cart = models.ManyToManyField('Dish', blank=True)
    groups = models.ManyToManyField(Group, related_name="customer_users")
    user_permissions = models.ManyToManyField(Permission, related_name="customer_user_permissions")
    
class Delivery(AbstractUser):
    first_name = models.CharField(max_length=30)  
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15)
    vehicles = models.CharField(max_length=50)
    wallet = models.DecimalField(max_digits=10, decimal_places=2) 
    groups = models.ManyToManyField(Group, related_name="delivery_users")
    user_permissions = models.ManyToManyField(Permission, related_name="delivery_user_permissions")

class Order(models.Model):
    order_id = models.IntegerField()  
    delivery_id = models.IntegerField(max_length=50)
    customer_id = models.IntegerField(max_length=50) 
    restaurant_id = models.IntegerField(max_length=50) 
    dishes_id = models.ManyToManyField('Dish')