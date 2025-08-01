from rest_framework import serializers
from product.models import Product, Category, Tags



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class PaymentSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=100, required=True)
    expiry_month = serializers.CharField(max_length=100, required=True)
    expiry_year = serializers.CharField(max_length=100, required=True)
    cvc = serializers.CharField(max_length=100, required=True)
