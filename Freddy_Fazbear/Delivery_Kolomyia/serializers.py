from rest_framework import serializers
from .models import Dish,Customer

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'