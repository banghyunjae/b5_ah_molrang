from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('signup/', views.UserView.as_view(), name='user_view'),
    path('login/', views.CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('', views.UserDetailView.as_view(), name='user_detail_view'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:pk>/',views.ProfileView.as_view(), name='profile_view'),
    path('<int:pk>/product/',views.ProfileProductView.as_view(), name='profile_product_view'),
    path('<int:pk>/wish/',views.ProfileWishView.as_view(), name='profile_wish_view'),
    path('<int:pk>/review/',views.ProfileReviewView.as_view(), name='profile_review_view'),
]
