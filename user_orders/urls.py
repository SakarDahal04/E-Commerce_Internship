
from user_orders.views import AddressViewSet, OrderViewSet, OrderItemViewSet, PaymentViewSet, UserViewSet
from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView






# Router for automatically generating URL patterns
router = routers.DefaultRouter()
router.register(r'address', AddressViewSet, basename = 'address')
router.register(r'orders', OrderViewSet, basename = 'order')
router.register(r'order-items', OrderItemViewSet, basename = 'order-item')
router.register(r'payments', PaymentViewSet, basename = 'payment')
router.register(r'users', UserViewSet, basename = 'user')


urlpatterns = [

    #path('login/', LoginView.as_view(), name='login'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)), 
]
