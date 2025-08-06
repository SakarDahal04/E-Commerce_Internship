from django.contrib import admin

# Register your models here.
from product.models import Category, Tags, Product, ProductTags, Review

admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Product)
admin.site.register(ProductTags)
admin.site.register(Review)


