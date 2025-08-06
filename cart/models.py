from django.db import models
from django.contrib.auth.models import User
from product.models import Product

import uuid

# Create your models here.
class AbstractDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Cart(AbstractDateModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.user}"

class CartItem(AbstractDateModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selected_for_checkout = models.BooleanField(default=False)

    @property
    def cartitem_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"Cart Item: {self.product.name}"