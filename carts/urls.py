from django.urls import path
from .views import CartListAPIView, CartDetailAPIView, CartItemDetailAPIView

app_name = 'carts'

urlpatterns = [
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('<int:pk>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('items/<int:pk>/', CartItemDetailAPIView.as_view(),
         name='cart-item-detail'),
]
