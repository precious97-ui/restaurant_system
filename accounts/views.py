from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# SIGNUP VIEW
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


# DASHBOARD VIEW
@login_required  # only logged-in users can access
def dashboard(request):
    return render(request, 'dashboard.html')