from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Product


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
