from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile  # make sure your Profile model has a phone field

# -----------------------------
# SIGNUP FORM
# -----------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, max_length=15, help_text="Optional, digits only")

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            # Save the phone in Profile
            phone = self.cleaned_data.get("phone")
            Profile.objects.update_or_create(user=user, defaults={"phone": phone})
        return user


# -----------------------------
# LOGIN FORM
# -----------------------------
class CustomAuthenticationForm(forms.Form):
    identifier = forms.CharField(label="Username / Email / Phone")
    password = forms.CharField(widget=forms.PasswordInput)