from django.db import models
from django.contrib.auth.models import User

# -----------------------------
# ORDER MODEL
# -----------------------------
class Order(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.food_item} x{self.quantity}"


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
        return f"{self.user.username} - {self.food_item} x{self.quantity} ({'Ordered' if self.ordered else 'In Cart'})"