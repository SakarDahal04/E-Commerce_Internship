from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
    SimpleRateThrottle,
)
from rest_framework import generics
from product.api.serializers import (
    ProductSerializer,
    ProductTagSerializer,
    CategorySerialzier,
    TagSerializer,
    PaymentSerializer,
    ReviewSerializer,
)

from django.conf import settings
from product.models import Product, ProductTags, Category, Tags, Review
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CustomProductThrottle(SimpleRateThrottle):
    scope = "custom"


class ProductListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    queryset = Product.objects.select_related("category").prefetch_related(
        "product_producttags_tag_id"
    )
    # throttle_classes = [AnonRateThrottle]
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("name")
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["category", "tags", "price"]
    search_fields = ["name"]

    # filter and searches..
    # filter using price as well as tags, categories.
    # searches using product name

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    # @method_decorator(cache_page(60 * 60 * 2))
    # here the first argument is timeout in seconds, so it's 2 hours in total.
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
    # queryset = Product.objects.select_related('category', 'tags').all()
    # did this but it limits product to only one tag
    queryset = Product.objects.all()
    

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = CategorySerialzier
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(60 * 60 * 2))
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
    queryset = Category.objects.all().order_by("name")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TagListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = TagSerializer
    queryset = Tags.objects.all().order_by("name")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    filter_backends = [filters.SearchFilter]

    search_fields = ["name"]

    @method_decorator(cache_page(60 * 60 * 2))
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

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProductTagsListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = ProductTagSerializer
    queryset = ProductTags.objects.select_related("product")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductTagsDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ProductTagSerializer
    queryset = ProductTags.objects.select_related("product")

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):

    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related("product").all()

    filter_backends = [filters.SearchFilter]
    filterset_fields = ["rating"]
    search_fields = ["product"]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ReviewDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related("product").all()

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


def delete(self, request, *args, **kwargs):
    return self.destroy(request, *args, **kwargs)


class StripeAPIPayment(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = PaymentSerializer
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data_dict = {}
        if not serializer.is_valid():
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
        payment_intent = stripe.PaymentIntent.create(
            amount=100, currency="inr", payment_method=payment_method.id, confirm=True
        )
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
