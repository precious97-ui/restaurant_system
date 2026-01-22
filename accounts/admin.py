from django.contrib import admin
from .models import Order, CartItem, MenuItem, Profile, TeamMember  # Added Profile and TeamMember


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


# -----------------------------
# PROFILE ADMIN
# -----------------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email_verified')
    search_fields = ('user__username', 'phone_number')


# -----------------------------
# TEAM MEMBER ADMIN
# -----------------------------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')
    search_fields = ('name', 'role')