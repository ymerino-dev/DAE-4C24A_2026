from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for categories."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """Provide CRUD endpoints for products with optional category filtering."""

    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        # Avoid one extra query per product when serializing the category.
        queryset = Product.objects.select_related('category').order_by('id')
        category_id = self.request.query_params.get('category')

        if category_id:
            try:
                queryset = queryset.filter(category_id=int(category_id))
            except (TypeError, ValueError):
                queryset = queryset.none()

        return queryset
