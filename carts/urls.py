from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet

router = DefaultRouter()
router.register('', CartViewSet, basename='carts')

urlpatterns = [
    path('carts/', include(router.urls)),  # 127.0.0.1:8000/carts/ 로 접속
]
