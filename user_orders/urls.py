
from user_orders.views import AddressViewSet, OrderViewSet, OrderItemViewSet, PaymentViewSet, UserViewSet, LoginView
from rest_framework import routers
from django.urls import path, include





# Router for automatically generating URL patterns
router = routers.DefaultRouter()
router.register(r'address', AddressViewSet, basename = 'address')
router.register(r'orders', OrderViewSet, basename = 'order')
router.register(r'order-items', OrderItemViewSet, basename = 'order-item')
router.register(r'payments', PaymentViewSet, basename = 'payment')
router.register(r'users', UserViewSet, basename = 'user')


urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)), 
]
