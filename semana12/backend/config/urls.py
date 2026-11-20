"""URL configuration for the config project."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import MovieViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
