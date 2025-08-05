from rest_framework import serializers
from product.models import Product, Category, Tags, Review


class CategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__" 


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerialzier()
    tags = TagSerializer()
    class Meta:
        model = Product
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Review
        fields = "__all__"

class PaymentSerializer(serializers.Serializer):
    card_number = serializers.IntegerField()
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    cvc = serializers.IntegerField()
