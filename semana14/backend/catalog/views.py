from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    LoginSerializer,
    ProductSerializer,
    UserSerializer,
)


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


class LoginView(APIView):
    """Return an authentication token for valid credentials."""

    # Keep the login endpoint public even if a stale token is sent.
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )

        if user is None:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )
