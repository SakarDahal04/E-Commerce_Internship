from django.urls import path
from product.api.views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    TagListCreateAPIView,
    TagDetailAPIView,
    StripeAPIPayment,
)

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path(
        "categories/",
        CategoryListCreateAPIView.as_view(),
        name="categories-list-create",
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailAPIView.as_view(),
        name="categories-detail",
    ),
    path("tags/", TagListCreateAPIView.as_view(), name="tags-list-create"),
    path("tags/<int:pk>/", TagDetailAPIView.as_view(), name="tags-detail"),
    path("payment/", StripeAPIPayment.as_view(), name="stripe-create-execute"),
]
