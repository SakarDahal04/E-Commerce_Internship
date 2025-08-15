from rest_framework import serializers
from product.models import Product, Category, Tags, Review, ProductTags


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"
        extra_fields = ["average_rating"]

    def get_average_rating(self, obj):
        reviews = obj.review_product.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 2)


class ProductTagSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    tag_id = TagSerializer()

    class Meta:
        model = ProductTags
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    # aba average rating kasari calculate garne ta
    class Meta:
        model = Review
        fields = "__all__"


class PaymentSerializer(serializers.Serializer):
    card_number = serializers.IntegerField()
    expiry_month = serializers.IntegerField()
    expiry_year = serializers.IntegerField()
    cvc = serializers.IntegerField()
