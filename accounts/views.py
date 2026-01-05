from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Order, CartItem  # make sure CartItem model exists in models.py

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
            return redirect('dashboard')  # redirect to dashboard
        else:
            # show form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


# -----------------------------
# DASHBOARD VIEW
# -----------------------------
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


# -----------------------------
# PLACE ORDER VIEW
# -----------------------------
@login_required
def place_order(request):
    if request.method == 'POST':
        food_item = request.POST.get('food_item')
        quantity = int(request.POST.get('quantity', 1))
        spice_level = request.POST.get('spice_level')
        salt_level = request.POST.get('salt_level')
        notes = request.POST.get('notes')

        # Save order to database
        Order.objects.create(
            user=request.user,
            food_item=food_item,
            quantity=quantity,
            spice_level=spice_level,
            salt_level=salt_level,
            notes=notes
        )

        messages.success(request, f"✅ Your order for {food_item} has been placed!")
        return redirect('dashboard')


# -----------------------------
# CART VIEWS
# -----------------------------
@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    return render(request, 'cart.html', {'items': items})


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        food_item = request.POST.get('food_item')
        quantity = int(request.POST.get('quantity', 1))
        spice_level = request.POST.get('spice_level')
        salt_level = request.POST.get('salt_level')
        notes = request.POST.get('notes')

        CartItem.objects.create(
            user=request.user,
            food_item=food_item,
            quantity=quantity,
            spice_level=spice_level,
            salt_level=salt_level,
            notes=notes
        )

        messages.success(request, f"🛒 {food_item} added to cart!")
    return redirect('dashboard')


@login_required
def remove_from_cart(request, item_id):
    try:
        item = CartItem.objects.get(id=item_id, user=request.user, ordered=False)
        item.delete()
        messages.success(request, "❌ Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect('cart')


@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    if items.exists():
        for item in items:
            item.ordered = True
            item.save()
        messages.success(request, "🎉 Your order has been placed successfully!")
    else:
        messages.info(request, "Your cart is empty!")
    return redirect('dashboard')


@login_required
def cart(request):
    # Query all CartItems that belong to the logged-in user and are not yet ordered
    from .models import CartItem
    cart_items = CartItem.objects.filter(user=request.user, ordered=False)
    
    return render(request, 'cart.html', {'cart_items': cart_items})