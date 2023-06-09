from django.urls import path
from articles import views


urlpatterns = [

    path("", views.ProductView.as_view(), name="product_view"),
    path("<int:id_product>/", views.ProductDetailView.as_view(), name="product_view"),
    path('<int:id_product>/wish/', views.WishView.as_view(), name='wish_view'),
    path("<int:id_product>/reviews/",
         views.ReviewView.as_view(), name="review-view"),
    path(
        "<int:id_product>/reviews/<int:id_review>/",
        views.ReviewDetailView.as_view(),
        name="review-detail_view",
    ),
]
