from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    spice_level = models.CharField(max_length=10, choices=SPICE_CHOICES)
    salt_level = models.CharField(max_length=10, choices=SALT_CHOICES)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_updated_at = models.DateTimeField(auto_now=True)       # ✅ Track when status last updated
    email_sent = models.BooleanField(default=False)               # ✅ Track if "delivered" email was sent
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name if self.menu_item else 'Unknown'} ({self.status})"


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
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    spice_level = models.CharField(max_length=10, choices=SPICE_CHOICES)
    salt_level = models.CharField(max_length=10, choices=SALT_CHOICES)
    notes = models.TextField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Ordered" if self.ordered else "In Cart"
        return f"{self.user.username} - {self.menu_item.name if self.menu_item else 'Unknown'} x{self.quantity} ({status})"


# -----------------------------
# MENU ITEM MODEL
# -----------------------------
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main', 'Main Dish'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    default_spice = models.CharField(max_length=10, choices=[('Low','Low'),('Medium','Medium'),('Hot','Hot')], default='Medium')
    default_salt = models.CharField(max_length=10, choices=[('Low','Low'),('Normal','Normal'),('Extra','Extra')], default='Normal')
    image = CloudinaryField('image', blank=True, null=True)  # Cloudinary
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -----------------------------
# PROFILE MODEL
# -----------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# -----------------------------
# TEAM MEMBER MODEL
# -----------------------------
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    photo = CloudinaryField('photo', blank=True, null=True)  # Cloudinary
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.role}"