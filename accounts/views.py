from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Order, CartItem, MenuItem, Profile, TeamMember
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# -----------------------------
# XAF Conversion Rate
# -----------------------------
XAF_RATE = 600  # 1 USD = 600 XAF

# -----------------------------
# DASHBOARD CATEGORIES
# -----------------------------
CATEGORIES = {
    'appetizer': 'Appetizers',
    'main': 'Main Dishes',
    'dessert': 'Desserts',
    'drink': 'Drinks'
}

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
            user = authenticate(request, username=identifier, password=password)

            if user is None:
                user_obj = User.objects.filter(email__iexact=identifier).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)

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
    search_query = request.GET.get('search', '').strip()
    selected_category = request.GET.get('category', '')

    if search_query:
        menu_items = menu_items.filter(name__icontains=search_query)
    if selected_category:
        menu_items = menu_items.filter(category__iexact=selected_category)

    for item in menu_items:
        item.price_xaf = item.price * XAF_RATE

    return render(request, 'dashboard.html', {
        'menu_items': menu_items,
        'search_query': search_query,
        'categories': CATEGORIES.items(),
        'selected_category': selected_category
    })

# -----------------------------
# ADD TO CART
# -----------------------------
@login_required
def place_order(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('menu_item_id')
        quantity = int(request.POST.get('quantity', 1))
        spice_level = request.POST.get('spice_level')
        salt_level = request.POST.get('salt_level')
        notes = request.POST.get('notes')

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            messages.error(request, "❌ Menu item does not exist.")
            return redirect('dashboard')

        CartItem.objects.create(
            user=request.user,
            menu_item=menu_item,
            quantity=quantity,
            spice_level=spice_level,
            salt_level=salt_level,
            notes=notes,
            ordered=False
        )
        messages.success(request, f"✅ '{menu_item.name}' has been added to your cart!")
    return redirect('dashboard')

# -----------------------------
# VIEW CART
# -----------------------------
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user, ordered=False)
    grand_total = 0

    for item in items:
        if item.menu_item:
            item.total_price_xaf = item.menu_item.price * item.quantity * XAF_RATE
            grand_total += item.total_price_xaf
        else:
            item.total_price_xaf = 0

    return render(request, 'cart.html', {'cart_items': items, 'grand_total': grand_total})

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
    if not items.exists():
        messages.info(request, "Your cart is empty!")
        return redirect('dashboard')

    for item in items:
        item.ordered = True
        item.save()

        Order.objects.create(
            user=item.user,
            menu_item=item.menu_item,
            quantity=item.quantity,
            spice_level=item.spice_level,
            salt_level=item.salt_level,
            notes=item.notes
        )

    messages.success(request, "🎉 Your order has been placed successfully!")
    return redirect('dashboard')

# -----------------------------
# ORDER HISTORY
# -----------------------------
@login_required
def order_history(request):
    orders = Order.objects.all().order_by('-created_at')  # Show all orders to staff
    return render(request, 'order_history.html', {'orders': orders})

# -----------------------------
# ABOUT PAGE
# -----------------------------
@login_required
def about(request):
    team_members = TeamMember.objects.all()
    return render(request, 'about.html', {'team_members': team_members})

# -----------------------------
# UPDATE ORDER STATUS (NEW)
# -----------------------------
@login_required
def update_order_status(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "❌ You are not authorized to update order status.")
        return redirect('order_history')

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'preparing', 'delivered']:
            order.status = new_status
            order.save()

            # Send email when order is delivered
            if new_status == 'delivered':
                profile = Profile.objects.filter(user=order.user).first()
                if profile and order.user.email:
                    send_mail(
                        subject="🍔 Your order is delivered!",
                        message=f"Hi {order.user.username}, your order '{order.menu_item.name}' has been delivered. Enjoy your meal!",
                        from_email="foody@localhost",
                        recipient_list=[order.user.email],
                        fail_silently=True
                    )

            messages.success(request, f"✅ Order status updated to {new_status.capitalize()}.")
        else:
            messages.error(request, "❌ Invalid status.")
    return redirect('order_history')