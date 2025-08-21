from django.urls import path
from cart.views import CartItemAddAPIView, CartItemListView, CheckoutRequestView, stripe_webhook

urlpatterns = [
    # path('my-cart/', views.CartRetrieveAPIView.as_view(), name="cart-info"),
    # path('carts/', views.CartListAPIView.as_view(), name="cart-list"),
    # path("carts/<int:pk>/activate/", views.CartActivateAPIView.as_view(), name="cart-activate"),
    # path('item-edit/<int:pk>/', views.CartItemRetrieveUpdateDestroyAPIView.as_view(), name='cart-item-edit'),
    # path('items/select/', views.BulkDataUpdateAPIView.as_view(), name='cart-items-bulk-select'),    # multiple items from the cart selected
    # path('checkout/', views.OrderCheckoutCreateAPIView.as_view(), name='checkout'),


    path('add-item/',CartItemAddAPIView.as_view(), name='cart-item-add'),
    path("list-cart/", CartItemListView.as_view(), name="list-cart"),
    path("checkout-request/", CheckoutRequestView.as_view(), name="checkout-request"),
    path("stripe-webhook/", stripe_webhook, name='stripe-webhook-endpoint'),

    # path("update-cart/<int:pk>/", views.CartItemUpdateView.as_view(), name="update-cart"),
    # path('create-stripe-session/', views.StripeCheckoutSessionAPIView.as_view(), name="stripe-session"),
    # path('payment-success/', views.payment_success, name='payment-success'),
    # path('payment-cancel/', views.payment_cancel, name='payment-cancel'),
    # path('stripe-webhook/', views.StripeWebhook.as_view(), name="stripe-webhook"),

]