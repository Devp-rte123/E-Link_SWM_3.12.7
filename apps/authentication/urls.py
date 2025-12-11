"""
URL patterns for the authentication app.
"""

# Import future annotations for forward references.
from __future__ import annotations

# Imported path for URL pattern definitions.
from django.urls import path

# Imported views from the authentication app.
from apps.authentication import views

# URL patterns for authentication views.
urlpatterns = [
    # /auth/login/
    path("login/", views.login_view, name="login"),
    # /auth/register/
    path("register/", views.register_view, name="register"),
    # /auth/logout/
    path("logout/", views.logout_view, name="logout"),
    # /auth/password-reset/ and related paths
    # for password reset workflow  
    # handled by views.password_reset_request_view
    path("password-reset/", views.password_reset_request_view, name="password_reset"),
    # handled by views.password_reset_confirm_view with uidb64 and token parameters
    path(
        "password-reset/<uidb64>/<token>/",
        views.password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    # handled by views.password_reset_request_view
    # for secure password reset links
    # and a done view
    path(
        "password-reset/done/",
        views.password_reset_request_view,  # or a separate success view
        name="password_reset_done",
    ),
]