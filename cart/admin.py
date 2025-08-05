from django.contrib import admin

from cart.models import Cart, CartItem, Product, OrderItem, Order
# Register your models here.


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)



