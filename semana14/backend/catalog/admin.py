from django.contrib import admin

from .models import Category, Order, OrderItem, Product


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


class OrderItemInline(admin.TabularInline):
    """Edit order items inside the order form."""

    model = OrderItem
    extra = 1


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin configuration for order items."""

    list_display = ('id', 'order', 'product', 'quantity', 'unit_price')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'order__user__username')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for orders with editable item lines."""

    inlines = (OrderItemInline,)
    list_display = ('id', 'user', 'created_at', 'status', 'total')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
