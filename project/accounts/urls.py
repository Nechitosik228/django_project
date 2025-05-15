from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views.views import (
    register,
    login_view,
    logout_view,
    profile,
    edit_profile_view,
    confirm_email,
    confirm_register,
)

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("confirm-register/", confirm_register, name="confirm_register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("accounts:password_change_done"),
            template_name="password_change.html",
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("edit-profile/", edit_profile_view, name="edit_profile"),
    path("confirm_email/", confirm_email, name="confirm_email"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset/form.html",
            email_template_name="password_reset/email.html",
            success_url="done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset/done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset/confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset/complete.html"
        ),
        name="password_reset_complete",
    ),
]
