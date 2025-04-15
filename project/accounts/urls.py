from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import register, login_view, logout_view, profile, edit_profile_view, confirm_email

app_name = "accounts"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy("accounts:password_change_done"), template_name="password_change.html"), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path("confirm_email", confirm_email, name="confirm_email"),
]