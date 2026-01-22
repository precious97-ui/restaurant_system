from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from django.contrib.auth import views as auth_views

# Redirect default homepage to login
def home(request):
    return redirect('custom_login')  # now points to our custom login view

urlpatterns = [
    path('', home),  # default redirects to custom login
    path('admin/', admin.site.urls),
    
    # Password reset URLs
    path('accounts/password-reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('accounts/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('accounts/', include('accounts.urls')),  # custom signup, add-to-cart, etc.
    path('dashboard/', views.dashboard, name='dashboard'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)