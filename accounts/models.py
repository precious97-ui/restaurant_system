from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# ORDER MODEL
# -----------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
    ]

    SPICE_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('Hot', 'Hot')
    ]

    SALT_CHOICES = [
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('Extra', 'Extra')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    spice_level = models.CharField(max_length=10, choices=SPICE_CHOICES)
    salt_level = models.CharField(max_length=10, choices=SALT_CHOICES)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item} ({self.status})"


# -----------------------------
# CART ITEM MODEL
# -----------------------------
class CartItem(models.Model):
    SPICE_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('Hot', 'Hot')
    ]

    SALT_CHOICES = [
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('Extra', 'Extra')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    spice_level = models.CharField(max_length=10, choices=SPICE_CHOICES)
    salt_level = models.CharField(max_length=10, choices=SALT_CHOICES)
    notes = models.TextField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Ordered" if self.ordered else "In Cart"
        return f"{self.user.username} - {self.food_item} x{self.quantity} ({status})"


# -----------------------------
# MENU ITEM MODEL
# -----------------------------
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    spice_level_choices = [('Low', 'Low'), ('Medium', 'Medium'), ('Hot', 'Hot')]
    salt_level_choices = [('Low', 'Low'), ('Normal', 'Normal'), ('Extra', 'Extra')]
    default_spice = models.CharField(max_length=10, choices=spice_level_choices, default='Medium')
    default_salt = models.CharField(max_length=10, choices=salt_level_choices, default='Normal')
    image_url = models.URLField(blank=True, null=True)  # optional image for menu
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name