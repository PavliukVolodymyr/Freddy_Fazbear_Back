from django.urls import path,include
from rest_framework import routers
from .views import ItemViewSet,CustomerViewSet,RestaurantViewSet,CartItemViewSet
from Delivery_Kolomyia import views
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'Dishes', ItemViewSet)
router.register(r'Customers',CustomerViewSet)
router.register(r'Restaurants',RestaurantViewSet)
router.register(r'Cart-items', CartItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', views.Auth, name='Auth'),
    path('check_token/', views.get_customer_id_by_token, name='Check_token'),
    path('register_customer/', views.register_customer),
    path('add_dish_to_cart/', views.add_dish_to_cart)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
