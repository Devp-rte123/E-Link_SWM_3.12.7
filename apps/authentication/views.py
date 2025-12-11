"""
Presentation-layer views for authentication.
"""
# Import future annotations for forward references.
from __future__ import annotations

# Imported auth for login/logout handling.
# Imported messages for user feedback.
from django.contrib import auth, messages
# Imported login_required decorator for protected views.
from django.contrib.auth.decorators import login_required
# Imported get_user_model to access the User model.
from django.contrib.auth import get_user_model
# Imported default_token_generator for token generation.
from django.contrib.auth.tokens import default_token_generator
# Imported types for request/response.
# Imported HttpRequest for typing.
# Imported HttpResponse for typing.
from django.http import HttpRequest, HttpResponse
# Imported shortcuts for rendering and redirects.
from django.shortcuts import redirect, render
# Imported for URL-safe base64 decoding.
from django.utils.http import urlsafe_base64_decode

# Imported forms for handling user input.
# Imported LoginForm for login view.
# Imported RegistrationForm for register view.
from apps.authentication.forms import LoginForm, RegistrationForm
# Imported DI container to get domain services.
# Imported get_user_service for user-related operations.
from apps.core.di.container import get_user_service

# Imported forms for password reset views.
# Imported PasswordResetRequestForm for requesting password reset.
# Imported PasswordResetConfirmForm for confirming password reset.
from apps.authentication.forms import (
    PasswordResetRequestForm,
    PasswordResetConfirmForm,
)
# Imported domain entities for type hints.
# Imported UserId for parameter types.
# Imported UserId
from apps.core.entities.user import UserId

# Get the Django user model.
# Used in views for user retrieval.
UserModel = get_user_model()

# View for user login.
# Handles GET/POST for login form.
# Uses LoginForm to validate credentials.
# Uses UserService for domain-level checks.
# Logs user in via django.contrib.auth.login.
# Persists login in session.
# Redirects to dashboard or next param on success.
# Renders login template with form on GET or validation errors.
# View for user login.
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle GET/POST for user login.

    - Validates credentials using LoginForm (Django auth backend).
    - Uses UserService for any domain checks (e.g. user must exist/active).
    - Logs the user in via django.contrib.auth.login.
    """
    user_service = get_user_service()  # DI: obtain service from container

    if request.method == "POST":
        # Bind POST data and current request to the form.
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            # Django user instance returned by the form.
            user = form.get_user()

            # Optional: use domain service for extra checks.
            user_entity = user_service.get_user_for_login(user.email)
            if user_entity is None:
                # Domain layer thinks this user should not log in.
                form.add_error(None, "User not allowed to log in.")
            else:
                # Persist login in the session.
                auth.login(request, user)
                messages.success(request, "Logged in successfully.")
                # Redirect to dashboard or next param.
                next_url = request.GET.get("next", "public_dashboard")
                return redirect(next_url)
    else:
        # For GET, show an empty login form.
        form = LoginForm(request=request)

    # Render template with form (and any validation errors).
    return render(request, "authentication/login.html", {"form": form})

# View for user logout.
# Logs out the current user.
# Redirects to login page with message.
# View for user logout.
@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Log out the current user and redirect to login.
    """
    auth.logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# View for user registration.
# Handles GET/POST for registration form.
# Uses RegistrationForm to validate input.
# Uses UserService to register new user.
# On success, redirects to login with message.
# Renders registration template with form on GET or validation errors.
# View for user registration.
def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle GET/POST for user registration.
    """
    user_service = get_user_service()  # obtain service via DI

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                # Delegate business logic to the domain service.
                user_service.register_user(
                    first_name=cd["first_name"],
                    last_name=cd["last_name"],
                    email=cd["email"],
                    phone_no=cd.get("phone_no"),
                    mobile_no=cd.get("mobile_no"),
                    address=cd.get("address"),
                    organization=cd.get("organization"),
                    password=cd["password1"],
                )
            except ValueError as exc:
                # Domain validation error (e.g. duplicate email).
                form.add_error("email", str(exc))
            else:
                messages.success(request, "Account created. Please log in.")
                return redirect("login")  # named URL for login view
    else:
        # For GET, show an empty form.
        form = RegistrationForm()

    # Render template with form (either empty or with errors).
    return render(request, "authentication/register.html", {"form": form})

# View for password reset request.
# Step 1: Ask for email and send reset link.
# Uses UserService.start_password_reset() for domain logic.
# View for password reset request.
def password_reset_request_view(request: HttpRequest) -> HttpResponse:
    """
    Step 1: Ask for email and send reset link.

    Uses UserService.start_password_reset() for domain logic.
    """
    user_service = get_user_service()

    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            uid_token = user_service.start_password_reset(email=email)

            # Always show success message, even if email not found.
            # Actual email sending is omitted here (plug your mailer).
            messages.info(
                request,
                "If an account exists for that email, a reset link has been sent.",
            )
            return redirect("password_reset_done")
    else:
        form = PasswordResetRequestForm()

    return render(
        request,
        "authentication/password_reset.html",
        {"form": form},
    )
    
# View for password reset confirmation.
# Step 2: Validate token and let the user choose a new password.
# - Decodes UserId/uidb64 to find the user.
# - Verifies the token with Django's default_token_generator.
# - Delegates the actual password update to UserService.
# View for password reset confirmation.  
def password_reset_confirm_view(
    request: HttpRequest, uidb64: str, token: str
) -> HttpResponse:
    """
    Step 2: Validate token and let the user choose a new password.

    - Decodes uidb64 to find the user.
    - Verifies the token with Django's default_token_generator.
    - Delegates the actual password update to UserService.
    """
    user_service = get_user_service()

    # Try to decode the user id from the URL.
    try:
        uid = int(urlsafe_base64_decode(uidb64).decode())
        user = UserModel.objects.get(pk=uid)
    except (ValueError, TypeError, UserModel.DoesNotExist):
        user = None

    # If user not found or token invalid, abort.
    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, "Invalid or expired password reset link.")
        return redirect("password_reset")

    if request.method == "POST":
        # Bind Django's SetPasswordForm to the user.
        form = PasswordResetConfirmForm(user, request.POST)
        if form.is_valid():
            # Use domain service to persist the new password.
            user_id = UserId(user.pk)
            user_service.finish_password_reset(
                user_id=user_id,
                new_password=form.cleaned_data["new_password1"],
            )
            messages.success(request, "Password updated. Please log in.")
            return redirect("login")
    else:
        # Initial GET, show empty password form.
        form = PasswordResetConfirmForm(user)

    # Render template with the form (and any validation errors).
    return render(
        request,
        "authentication/password_reset_confirm.html",
        {"form": form},
    )


