from .models import Address, Order, OrderItem, Payment
from rest_framework import serializers
from django.contrib.auth.models import User
from product.models import Product


from product.api.serializers import ProductSerializer
# Serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user'] 

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price']
        read_only_fields = ['id', 'status', 'total_price']

class OrderItemSerializer(serializers.ModelSerializer):
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product = ProductSerializer(read_only=True)
    order = OrderDetailsSerializer(read_only = True)
    
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'order']
        # read_only_fields = ['price']
   

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'updated_at', 'total_price', 'order_items']
        read_only_fields = ['created_at', 'updated_at', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        total_price = 0

        
        order = Order.objects.create(user=user, total_price=0)  

        
        # Step 2: Create OrderItem instances
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total_price += product.price * quantity

        # Step 3: Update total price on order
        order.total_price = total_price
        order.save()

        return order


    

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment

        fields = '__all__'
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active','password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "Password is required."})

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=validated_data.get('is_staff', False),
            is_active=validated_data.get('is_active', True),
            password=password  
        )
        return user
