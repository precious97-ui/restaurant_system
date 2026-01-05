"""
URL configuration for restaurant_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

# Redirect default homepage to login
def home(request):
    return redirect('login')  # use Django auth login URL name

urlpatterns = [
    path('', home),  # default redirects to login
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('accounts/', include('accounts.urls')),  # custom signup, add-to-cart, etc.
    path('dashboard/', views.dashboard, name='dashboard'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)