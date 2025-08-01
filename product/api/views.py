from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from product.api.serializers import (
    ProductSerializer,
    CategorySerialzier,
    TagSerializer,
    PaymentSerializer,
)
from django.conf import settings
from product.models import Product, Category, Tags
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = CategorySerialzier
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = CategorySerialzier
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TagListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = TagSerializer
    queryset = Tags.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TagDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = TagSerializer
    queryset = Tags.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StripeAPIPayment(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = PaymentSerializer
    queryset = Tags.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data_dict = {}
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        data_dict = serializer.validated_data
        card_details = {
            "type": "card",
            "card": {
                "number": data_dict["card_number"],
                "exp_month": data_dict["expiry_month"],
                "exp_year": data_dict["expiry_year"],
                "cvc": data_dict["cvc"],
            },
        }
        payment_method = stripe.PaymentMethod.create(**card_details)
        payment_intent = stripe.PaymentIntent.create(amount=100, currency="inr", payment_method=payment_method.id, confirm=True)
        payment_intent_modify = stripe.PaymentIntent.modify(
            payment_intent["id"], payment_method=payment_method.id
        )
        payment_intent_modify = stripe.PaymentIntent.retrieve(payment_intent["id"])
        if payment_intent_modify and payment_intent_modify["status"] == "succeeded":
            response = {
                "message": "payment is done, enjoy your service",
                "status": "done",
                "card_details": card_details,
            }
        else:
            response = {
                "message": "payment is NOT DONE ",
                "status": "bhag",
                "card_details": card_details,
            }
        return self.create(self, request, *args, **kwargs)
