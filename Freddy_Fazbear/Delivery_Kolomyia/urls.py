from django.urls import path,include
from rest_framework import routers
from .views import ItemViewSet,CustomerViewSet,RestaurantViewSet
from Delivery_Kolomyia import views
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'Dishes', ItemViewSet)
router.register(r'Customers',CustomerViewSet)
router.register(r'Restaurants',RestaurantViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', views.Auth, name='Auth')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
