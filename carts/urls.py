from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CartListCreateView,
    CartRetrieveUpdateDestroyView,
    CartItemRetrieveUpdateDestroyView,
    CartTotalPriceView,
    CartItemSelectionView,
)


app_name = 'carts'

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart-list-create'),
    path('<int:pk>/', CartRetrieveUpdateDestroyView.as_view(),
         name='cart-retrieve-update-destroy'),
    path('items/<int:pk>/', CartItemRetrieveUpdateDestroyView.as_view(),
         name='cart-item-retrieve-update-destroy'),
    path('total-price/', CartTotalPriceView.as_view(), name='cart-total-price'),
    path('items/<int:pk>/select/',
         CartItemSelectionView.as_view(), name='cart-item-select'),
    path('items/<int:pk>/deselect/',
         CartItemSelectionView.as_view(), name='cart-item-deselect'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
