from django.contrib import admin
from .models import *
from django.apps import apps

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Ця опція вказує, скільки об'єктів CartItem можна додавати одночасно

class CustomerAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

admin.site.register(Customer, CustomerAdmin)

all_models = apps.get_models()

for model in all_models:
    if not admin.site.is_registered(model):
        admin.site.register(model)
