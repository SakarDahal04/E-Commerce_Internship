from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Tags(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category"
    )
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name="product_tags")
    
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    


class ProductTags(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_producttags"
    )
    tag_id = models.ForeignKey(
        Tags, on_delete=models.CASCADE, related_name="tags_producttags"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    class Rating(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review_product")
    rating = models.IntegerField(choices=Rating.choices)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
