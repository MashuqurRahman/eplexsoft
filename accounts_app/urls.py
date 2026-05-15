from django.urls import path
from django.contrib.auth import views as auth_views
from .views import admin_registration_view, admin_login_view, user_authentication_view, user_logout_view, admin_logout_view
from .forms import CustomPasswordResetForm
urlpatterns = [ 
    path("auth/", user_authentication_view, name="user_auth"),
    path('logout/', user_logout_view, name='logout_url'),

    path('signup/', admin_registration_view, name='registration_url'),
    path('login/', admin_login_view, name='login_url'),
    path('admin-logout/', admin_logout_view, name='admin_logout_url'), 
    
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             form_class=CustomPasswordResetForm,
         ), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]