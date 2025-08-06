from rest_framework import serializers

from cart.models import Cart, CartItem, Product
from user_orders.models import Order, OrderItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", 'email')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock')


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),source='product', write_only=True)
    product = ProductSerializer(read_only=True)
    cartitem_subtotal = serializers.ReadOnlyField()

    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')

        if product and quantity:
            if quantity > product.stock:
                raise serializers.ValidationError({
                    "quantity": f"Only {product.stock} is available in the stock"
                })
        
        return attrs

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_id', 'quantity', 'selected_for_checkout', 'cartitem_subtotal')
        read_only_fields = ('product',)


class CartItemUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    def validate_selected_for_checkout(self, value):
        print("value during validation:", value)
        if value is None:
            raise serializers.ValidationError("Item is not selected for the checkout")

        value = True
        return value

    class Meta:
        model = CartItem
        fields = ["id", "quantity", "selected_for_checkout"]
        

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)


    def get_total_price(self, obj):
        order_items = obj.items.all()
        print(order_items)
        return sum(order_item.cartitem_subtotal for order_item in order_items)

    class Meta:
        model = Cart
        fields = ('user', 'created_at', 'updated_at', 'items', 'total_price')



class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="product.price")

    class Meta:
        model = OrderItem
        fields = ("product", "product_price", "quantity", "item_subtotal")

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Order
        fields = ('order_id', 'status', 'user', 'products')


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at', 'items')
        read_only_fields = ('order_id', 'created_at','user', 'items')

    def create(self, validated_data):
        user = self.context['request'].user

        cart = Cart.objects.prefetch_related('items__product').get(user=user)
        selected_items = cart.items.filter(selected_for_checkout=True)

        if not selected_items.exists():
            raise serializers.ValidationError("No items selected for checkout")

        order = Order.objects.create(user = user)

        order_items = []
        for item in selected_items:
            order_items.append(OrderItem(
                order = order,
                product = item.product,
                quantity = item.quantity,
            ))

        OrderItem.objects.bulk_create(order_items)

        selected_items.delete()

        return order