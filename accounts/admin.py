from django.contrib import admin
from .models import Order, CartItem, MenuItem  # Added MenuItem


# -----------------------------
# ORDER ADMIN
# -----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'food_item',
        'quantity',
        'created_at'
    )
    list_filter = ('created_at',)
    search_fields = ('user__username', 'food_item')


# -----------------------------
# CART ITEM ADMIN
# -----------------------------
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
    search_fields = ('user__username', 'food_item')


# -----------------------------
# MENU ITEM ADMIN
# -----------------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'default_spice',
        'default_salt',
        'created_at'
    )
    list_filter = ('default_spice', 'default_salt', 'created_at')
    search_fields = ('name', 'description')