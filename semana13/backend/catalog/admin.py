from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for categories."""

    list_display = ('id', 'name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for products."""

    list_display = ('id', 'name', 'category', 'price', 'stock', 'image')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'category__name')
