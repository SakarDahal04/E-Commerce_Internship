from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.models import User
from cart.models import Cart, CartItem 
from user_orders.models import Order, OrderItem
from product.models import Product
from cart.serializers import CartSerializer, CartItemSerializer, OrderCreateSerializer, CartItemUpdateSerializer, OrderSerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from decimal import Decimal

from django.contrib.auth import get_user_model
import stripe

# Create your views here.
class CartRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.select_related('user').prefetch_related('items', 'items__product').get_or_create(user=self.request.user)
        
        for c in cart.items.all():
            print(c)

        return cart


class CartItemAddAPIView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def perform_create(self, serializer):
        user = self.request.user
        cart,_ = Cart.objects.get_or_create(user=user)

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            print("-------------It will update--------------------")
        except CartItem.DoesNotExist:
            serializer.save(cart=cart)
            print("--------------------it will create new--------------------")


class CartItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    def get_queryset(self):
        items = CartItem.objects.select_related('product', 'cart__user').filter(cart__user = self.request.user)
        return items


class OrderCheckoutCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}
    

class BulkDataUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        items_data = request.data.get('items', [])
        if not isinstance(items_data, list) or not items_data:
            return Response(
                {"detail": "A non-empty list of items is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_count = 0
        for item_data in items_data:
            item_id = item_data.get("id")
            selected = item_data.get("selected_for_checkout")

            if item_id is None or selected is None:
                continue  # Skip incomplete entries

            try:
                if request.user.is_authenticated:
                    cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
                else:
                    cart_item = CartItem.objects.get(id=item_id)

                # cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
                cart_item.selected_for_checkout = selected
                cart_item.save(update_fields=["selected_for_checkout"])
                updated_count += 1
                print("done with the updation")
            except CartItem.DoesNotExist:
                print("cart item doesnt exist")
                continue  # Ignore invalid IDs

        return Response({"updated": updated_count, "next":"/cart/checkout/"}, status=status.HTTP_200_OK)
    
# Finalized view to run when we click on Cart in the Frontend
class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CartItem.objects.filter(cart__user=self.request.user)
        # print(queryset)
        return queryset


# View to run when the items are selected and checkout is clicked.
class CheckoutRequestView(APIView):
    permission_classes = [IsAuthenticated]

    # When the request from the frontend is sent, it should send back the list of 
    def patch(self, request):
        items_data = request.data
        print("Before the serializer",items_data)

        if not isinstance(items_data, list) or not items_data:
            return Response(
                {"detail": "Select at least one items for checkout"},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated_count = 0
        for item_data in items_data:
            try:
                instance = CartItem.objects.get(id=item_data['id'], cart__user=request.user)
                serializer = CartItemUpdateSerializer(instance, data=item_data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                print("Updated Data: ",serializer.data)
                updated_count += 1
            except CartItem.DoesNotExist:
                continue
        
        return Response({"updated": updated_count}, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        cart_items = CartItem.objects.filter(cart__user = user, selected_for_checkout=True)

        print("Obtained Cart Items for checkout", cart_items)

        if not cart_items.exists():
            return Response({"detail": "No items is selected for checkout"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validation for the checkout request and stock available
        total = Decimal("0.00")

        for item in cart_items:
            total += (item.quantity * item.product.price)
            if item.quantity > item.product.stock:
                return Response({
                    "detail": f"Not enough stock for {item.product.name} (Available: {item.product.stock})"
                }, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user, total_price=total, status="Pending")

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product = item.product,
                quantity = item.quantity,
                price = item.product.price * item.quantity,
                # item_subtotal = item.quantity * item.product.price
            )

            item.product.stock -= item.quantity

        cart_items.delete()

        return Response({
            "detail": "Order created successfully",
            "order_id": str(order.id),
            "total": str(order.total_price)
        }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        items_to_delete = request.data

        if not isinstance(items_to_delete, list) or not items_to_delete:
            return Response({
                "detail": "No items selected for delete",
            }, status=status.HTTP_400_BAD_REQUEST)

        for item_to_delete in items_to_delete:
            try:
                instance = CartItem.objects.get(id=item_to_delete['id'], cart__user=request.user)
                instance.delete()
            except CartItem.DoesNotExist:
                continue

        return Response({"deleted": "Items deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# class CartItemDeleteAPIView()


# class CartItemUpdateView(generics.RetrieveUpdateAPIView):
#     serializer_class = CartItemUpdateSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return CartItem.objects.filter(cart__user=self.request.user)


# # @method_decorator()
# class StripeCheckoutSessionAPIView(APIView):
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     template_name = 'cart/stripe.html'
#     # permission_classes = [IsAuthenticated]


#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):

#         hardcoded_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MzA5MzI3LCJpYXQiOjE3NTQzMDY5MjcsImp0aSI6ImI3ODBlMjU4MTlhODQwZGE4YzNlYjc1NzViM2RhYTRhIiwidXNlcl9pZCI6IjIifQ.uBUPhZKrPVuKy7ryWH3VLZvybok32ueS1QmSWCyKUdQ"

#         try:
#             validated_token = AccessToken(hardcoded_token)
#             user_id = validated_token['user_id']
#             user = User.objects.get(id=user_id)
#         except Exception as e:
#             return Response({"error": "Invalid hardcoded token"}, status=status.HTTP_401_UNAUTHORIZED)

#         order = Order.objects.get()
#         cart = Cart.objects.prefetch_related('items__product').get(user=user)
#         selected_items = cart.items.filter(selected_for_checkout=True)

#         if not selected_items.exists():
#             return Response({"error": "None of the items were selected for checkout"}, status=status.HTTP_400_BAD_REQUEST)

#         line_items = []
#         for item in selected_items:
#             line_items.append({
#                 "price_data": {
#                     "currency": "usd",
#                     "product_data": {
#                         "name": item.product.name
#                     },
#                     'unit_amount': int(item.product.price * 100)
#                 },
#                 "quantity": item.quantity
#             })
            
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             mode='payment',
#             # customer_email=request.user.email,
#             line_items=line_items,
#             success_url = "http://127.0.0.1:8000/cart/payment-success?session_id={CHECKOUT_SESSION_ID}/",
#             cancel_url = "http://127.0.0.1:8000/cart/payment-cancel/",
#             metadata={'user_id': user.id}
#         )

        

#         # return Response({'sessionId': checkout_session.id})

#         print("Redirecting to...", checkout_session.url)

#         return redirect(checkout_session.url)

# class StripeWebhook(APIView):
#     def post(self, request):
#         payload = request.data
#         sig_header = request.META.get('HTTP_STRIPE_HEADER')
#         endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#         # construct event for verifying webhook
#         try:
#             event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#             )
#         except ValueError as e:
#             # Invalid payload
#             print('Error parsing payload: {}'.format(str(e)))
#             return HttpResponse(status=400)
#         except stripe.error.SignatureVerificationError as e:
#             # Invalid signature
#             print('Error verifying webhook signature: {}'.format(str(e)))
#             return HttpResponse(status=400)

#         # Handle the event
#         if event.type == 'payment_intent.succeeded':
#             print(event)
#             payment_intent = event.data.object # contains a stripe.PaymentIntent
#             print('PaymentIntent was successful!')
#             order = Order.objects.get(stripe_checkout_session_id=payment_intent['id'])
#             order.is_paid = True
#             order.save()
#             return Response({'status': 'success'})
#         elif event.type == 'payment_method.attached':
#             payment_method = event.data.object # contains a stripe.PaymentMethod
#             print('PaymentMethod was attached to a Customer!')
#         # ... handle other event types
#         else:
#             print('Unhandled event type {}'.format(event.type))


# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except stripe.error.SignatureVerificationError:
#         return HttpResponse(status=400)

#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         user_id = session['metadata']['user_id']

#         User = get_user_model()
#         user = User.objects.get(id=user_id)

#         # now create order using your serializer or logic
#         cart = Cart.objects.prefetch_related('items__product').get(user=user)
#         selected_items = cart.items.filter(selected_for_checkout=True)

#         if selected_items.exists():
#             order = Order.objects.create(user=user)
#             order_items = []
#             for item in selected_items:
#                 order_items.append(OrderItem(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                 ))

#             OrderItem.objects.bulk_create(order_items)
#             selected_items.delete()

#     return HttpResponse(status=200)

# def payment_success(request):
#     # return Response({'success': "Payment Successful"})
#     # stripe_webhook(request)
#     return HttpResponse("Payment Successful")


# def payment_cancel(request):
#     # return Response({'cancel': "Payment Cancelled"})
#     return HttpResponse("Payment Failed")

