from .models import Address, Order, OrderItem, Payment
from rest_framework import serializers
from django.contrib.auth.models import User
from Products.models import Product
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user'] 


# Temporary Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "created_at"]
        read_only_fields = ["price"]



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    class Meta:
        model = OrderItem
        fields = ['product', 'product_id', 'quantity', 'price']
        read_only_fields = ['price']
   



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'created_at', 'updated_at', 'order_items']
        read_only_fields = ['status', 'total_price', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        total_price = 0

        
        order = Order.objects.create(user=user, total_price=0)  

        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price

            total_price += price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price
            )

        
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




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


