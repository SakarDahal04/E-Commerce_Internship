from .models import Address, Order, OrderItem, Payment
from rest_framework import serializers
from django.contrib.auth.models import User
from Products.models import Product
# Serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user'] 


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        read_only_fields = ['order', 'user', 'price']
        #exclude = ["order"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'total_price']

    def create(self, validated_data):
        order_items_data = validated_data.pop('items', [])
        user = self.context['request'].user

        total_price = 0

        for item_data in order_items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            total_price += product.price * quantity

        order = Order.objects.create(user=user, total_price=total_price, **validated_data)

        for item_data in order_items_data:
            item_data.pop('user', None)
            product = item_data['product']
            item_data['price'] = product.price  # Set price here
            OrderItem.objects.create(order=order, user=user, **item_data)

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
        password= validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({"password": "Password is required."})
        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            is_staff=validated_data.get('is_staff', False),
            is_active=validated_data.get('is_active', True)
        )

        return user
