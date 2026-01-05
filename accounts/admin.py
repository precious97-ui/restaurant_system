from django.contrib import admin
from .models import Order, CartItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'food_item',
        'quantity',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'food_item')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'food_item',
        'quantity',
        'ordered',
        'added_at'
    )
    list_filter = ('ordered',)