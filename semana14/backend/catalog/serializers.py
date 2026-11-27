from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import Category, Order, OrderItem, Product


class CategorySerializer(serializers.ModelSerializer):
    """Serialize categories."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """Serialize products with nested category data on read."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'image',
            'category',
            'category_id',
        ]


class UserSerializer(serializers.ModelSerializer):
    """Expose public user data."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class LoginSerializer(serializers.Serializer):
    """Validate the credentials submitted to the login endpoint."""

    username = serializers.CharField(trim_whitespace=False)
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )


class OrderItemSerializer(serializers.ModelSerializer):
    """Serialize order lines and validate their incoming product data."""

    product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_id',
            'quantity',
            'unit_price',
        ]
        read_only_fields = ['id', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    """Serialize orders with their items and create them atomically."""

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'total', 'items']
        read_only_fields = ['id', 'created_at', 'status', 'total']

    def validate_items(self, value):
        """Reject an order without items."""
        if not value:
            raise serializers.ValidationError('At least one item is required.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        """Create an order, reserve stock, and freeze current prices."""
        items_data = validated_data.pop('items')
        user = validated_data.pop('user')

        product_ids = [item['product_id'] for item in items_data]
        products = {
            product.id: product
            for product in Product.objects.select_for_update().filter(
                id__in=product_ids,
            )
        }

        missing_ids = set(product_ids) - set(products)
        if missing_ids:
            raise serializers.ValidationError({
                'items': (
                    'Unknown product ids: '
                    f'{sorted(missing_ids)}.'
                ),
            })

        planned_quantities = {}
        total = Decimal('0.00')

        for item_data in items_data:
            product = products[item_data['product_id']]
            quantity = item_data['quantity']
            reserved = planned_quantities.get(product.id, 0)
            available = product.stock - reserved

            if available < quantity:
                raise serializers.ValidationError({
                    'items': (
                        f'Insufficient stock for {product.name}. '
                        f'Available: {available}, requested: {quantity}.'
                    ),
                })

            planned_quantities[product.id] = reserved + quantity
            total += product.price * quantity

        order = Order.objects.create(user=user, total=total)

        for item_data in items_data:
            product = products[item_data['product_id']]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.price,
            )

        for product_id, quantity in planned_quantities.items():
            product = products[product_id]
            product.stock -= quantity
            product.save(update_fields=['stock'])

        return order
