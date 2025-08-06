# Imports
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
import stripe
from .models import Address, Order, OrderItem, Payment
from .serializers import AddressSerializer, OrderSerializer, OrderItemSerializer, PaymentSerializer, User, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from .permissions import IsOrderItemOwner, PermManager, IsObjectOwner, IsOrderOwner



# Create your views here

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsObjectOwner]
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Address.objects.filter(user = self.request.user)




@method_decorator(cache_page(60 * 15), name='list')
@method_decorator(cache_page(60 * 15), name='retrieve') 
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        print("Filtering orders for user:", self.request.user)
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    

@method_decorator(cache_page(60 * 15), name='list')
@method_decorator(cache_page(60 * 15), name='retrieve') 
class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_class = [IsAuthenticated, IsOrderItemOwner]

    serializer_class = OrderItemSerializer

    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_queryset(self):
        return OrderItem.objects.filter(user = self.request.user)
    
    def get_queryset(self):
        return OrderItem.objects.filter(order_user = self.request.user)

    def list(self, request, *args, **kwargs):
        raise PermissionDenied("Listing all items is not allowd")






class PaymentViewSet(viewsets.ModelViewSet):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_stripe_checkout(self, request):
        try:
            order_id = request.data.get('order_id')
            if not order_id:
                return Response({'error': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            order = Order.objects.filter(id=order_id, user=request.user).first()
            if not order:
                return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

            line_items = []
            for item in order.items.all():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.product.name},
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': item.quantity
                })
            if not line_items:
                return Response({'error': 'Order has no items.'}, status=status.HTTP_400_BAD_REQUEST)
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url='http://localhost:8000/success/',
                cancel_url='http://localhost:8000/cancel/',
            )
            return Response({'sessionId': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()
        


class LoginView(ObtainAuthToken):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    permission_classes = [AllowAny]
    authentication_classes = []
    

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        
   
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })