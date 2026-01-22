from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Order, CartItem, MenuItem, Profile, TeamMember
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Conversion rate USD -> XAF
XAF_RATE = 600  # adjust according to your needs

# -----------------------------
# SIGNUP VIEW
# -----------------------------
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone_number')
            if phone:
                Profile.objects.create(user=user, phone_number=phone)
            login(request, user)
            messages.success(request, f"🎉 Welcome, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# -----------------------------
# LOGIN VIEW
# -----------------------------
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier'].strip()
            password = form.cleaned_data['password']
            user = None

            # Try username
            user = authenticate(request, username=identifier, password=password)

            # Try email
            if user is None:
                user_obj = User.objects.filter(email__iexact=identifier).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)

            # Try phone number
            if user is None:
                profile = Profile.objects.filter(phone_number=identifier).first()
                if profile:
                    user = authenticate(request, username=profile.user.username, password=password)

            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "❌ Invalid username, email, or phone number")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# -----------------------------
# DASHBOARD VIEW
# -----------------------------
@login_required
def dashboard(request):
    menu_items = MenuItem.objects.all()
    for item in menu_items:
        item.price_xaf = item.price * XAF_RATE
    return render(request, 'dashboard.html', {'menu_items': menu_items})


# -----------------------------
# ADD TO CART
# -----------------------------
@login_required
def place_order(request):
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
            notes=notes,
            ordered=False
        )

        messages.success(request, f"✅ '{food_item}' has been added to your cart!")

    return redirect('dashboard')


# -----------------------------
# VIEW CART (with XAF totals)
# -----------------------------
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    grand_total = 0

    for item in items:
        menu_item = MenuItem.objects.filter(name=item.food_item).first()
        if menu_item:
            item.price_xaf = menu_item.price * XAF_RATE
            item.total_price_xaf = item.price_xaf * item.quantity
            grand_total += item.total_price_xaf

    return render(request, 'cart.html', {
        'cart_items': items,
        'grand_total': grand_total
    })


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

            # Save to order history
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
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


# -----------------------------
# ABOUT PAGE VIEW
# -----------------------------
@login_required
def about(request):
    team_members = TeamMember.objects.all()
    return render(request, 'about.html', {'team_members': team_members})