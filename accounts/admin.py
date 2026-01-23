from django.contrib import admin
from .models import Order, CartItem, MenuItem, Profile, TeamMember

# -----------------------------
# ORDER ADMIN
# -----------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'menu_item',  # updated here
        'quantity',
        'status',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'menu_item__name')  # updated here

# -----------------------------
# CART ITEM ADMIN
# -----------------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'menu_item',  # updated here
        'quantity',
        'spice_level',
        'salt_level',
        'ordered',
        'added_at'
    )
    list_filter = ('ordered', 'spice_level', 'salt_level')
    search_fields = ('user__username', 'menu_item__name')  # updated here

# -----------------------------
# MENU ITEM ADMIN
# -----------------------------
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'default_spice',
        'default_salt',
        'created_at'
    )
    list_filter = ('category', 'default_spice', 'default_salt', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'price', 'default_spice', 'default_salt', 'image')
        }),
    )

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