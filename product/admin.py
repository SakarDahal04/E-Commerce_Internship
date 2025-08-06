from django.contrib import admin

# Register your models here.
from product.models import Category, Tags

admin.site.register(Category)
admin.site.register(Tags)


