from django.db import models
from django.contrib.auth.models import User
from Products.models import Product



# Create your models here.

#address model
# This model is used to store user addresses for orders
# It includes a foreign key to the User model
class Address(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    street = models.CharField(max_length = 225)
    city = models.CharField(max_length = 100)
    state = models.CharField(max_length = 100)
    postal_code = models.CharField(max_length = 20)
    country = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.postal_code}, {self.country} - {self.user.username}"



#order model
# This model is used to store orders placed by users
# It includes a foreign key to the User model and a foreign key to the Product model
class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-created_at'] 
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"



#order items model
# This model is used to store items in an order
# It includes a foreign key to the Order model and a foreign key to the User model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='items')
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"Order Item {self.id} for Order {self.order.id} - {self.Product.name}"
    


#payment model
# This model is used to store payment information for an order
# It includes a foreign key to the Order model and a foreign key to the User model
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    payment_method = models.CharField(max_length = 50)
    payment_date = models.DateTimeField(auto_now_add = True)
    payment_status = models.CharField(max_length = 50, default = 'Pending')
    transaction_id = models.CharField(max_length = 100, unique = True)
