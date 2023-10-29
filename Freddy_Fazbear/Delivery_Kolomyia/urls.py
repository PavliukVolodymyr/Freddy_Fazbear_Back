from django.urls import path,include
from rest_framework import routers
from .views import ItemViewSet,CustomerViewSet

router = routers.DefaultRouter()
router.register(r'mymodels', ItemViewSet)
router.register(r'Customers',CustomerViewSet)

urlpatterns = [
    # ...
    path('api/', include(router.urls)),
]
