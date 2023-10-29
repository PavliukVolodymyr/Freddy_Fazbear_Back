from django.urls import path,include
from rest_framework import routers
from .views import ItemViewSet,CustomerViewSet
from Delivery_Kolomyia import views

router = routers.DefaultRouter()
router.register(r'mymodels', ItemViewSet)
router.register(r'Customers',CustomerViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', views.Auth, name='Auth')
]
