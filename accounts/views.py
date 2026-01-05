from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Order, CartItem, MenuItem  # Added MenuItem


# -----------------------------
# SIGNUP VIEW
# -----------------------------
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = request.POST.get('username')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f"❌ Username '{username}' is already taken.")
            return render(request, 'registration/signup.html', {'form': form})

        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            messages.success(request, f"🎉 Welcome, {username}! Your account has been created.")
            return redirect('dashboard')
        else:
            # Show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


# -----------------------------
# DASHBOARD VIEW (Dynamic Menu)
# -----------------------------
@login_required
def dashboard(request):
    menu_items = MenuItem.objects.all()  # Fetch all menu items from database
    return render(request, 'dashboard.html', {'menu_items': menu_items})


# -----------------------------
# PLACE ORDER (Add to Cart)
# -----------------------------
@login_required
def place_order(request):
    if request.method == 'POST':
        food_item = request.POST.get('food_item')
        quantity = int(request.POST.get('quantity', 1))
        spice_level = request.POST.get('spice_level')
        salt_level = request.POST.get('salt_level')
        notes = request.POST.get('notes')

        # Save to CartItem
        CartItem.objects.create(
            user=request.user,
            food_item=food_item,
            quantity=quantity,
            spice_level=spice_level,
            salt_level=salt_level,
            notes=notes,
            ordered=False
        )

        messages.success(request, f"✅ '{food_item}' has been added to your cart!")
    return redirect('dashboard')


# -----------------------------
# VIEW CART
# -----------------------------
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    return render(request, 'cart.html', {'cart_items': items})


# -----------------------------
# REMOVE FROM CART
# -----------------------------
@login_required
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, user=request.user, ordered=False)
        item.delete()
        messages.success(request, "❌ Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect('cart')


# -----------------------------
# CHECKOUT
# -----------------------------
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    if items.exists():
        for item in items:
            item.ordered = True
            item.save()
            # Optional: save to Orders for history
            Order.objects.create(
                user=item.user,
                food_item=item.food_item,
                quantity=item.quantity,
                spice_level=item.spice_level,
                salt_level=item.salt_level,
                notes=item.notes
            )
        messages.success(request, "🎉 Your order has been placed successfully!")
    else:
        messages.info(request, "Your cart is empty!")
    return redirect('dashboard')


# -----------------------------
# ORDER HISTORY
# -----------------------------
@login_required
def order_history(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})