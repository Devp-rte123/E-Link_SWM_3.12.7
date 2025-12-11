"""
Django forms for authentication views.
"""

# Import future annotations for forward references.
from __future__ import annotations

# Imported for login and registration forms.
from django import forms

# Imported for password setting form (if needed).
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm

# Imported for accessing the User model.
from django.contrib.auth import get_user_model

# Imported for URL-safe base64 encoding/decoding.
from django.utils.http import urlsafe_base64_decode

# Imported for password validation.
from django.contrib.auth import password_validation

# Imported for login form authentication.
from django.contrib.auth import authenticate

# Get the Django user model.
# Used in forms for validation and user retrieval.
UserModel = get_user_model()


# Login form used by the login view.
# Delegates credential checking to Django's authenticate().
# The view can then use the authenticated user.
class LoginForm(forms.Form):
    """
    Login form that delegates credential check to Django's authenticate().
    """

    # ---------- form fields ----------
    # Define username and password fields with widgets
    # ---------- form fields ----------
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username or Email"}
        ),
        error_messages={"required": "Username or Email is required."},
    )  # email or username
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        error_messages={"required": "Password is required."},
    )

    #  ---------- internal state ----------
    # Cache for authenticated user after validation
    # ---------- internal state ----------
    def __init__(self, *args, **kwargs):
        # The view passes request so authenticate() can use it if needed.
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self._user = None  # cache for authenticated user

    # ---------- cross-field validation ----------
    # Check credentials using Django's authenticate()
    # If valid, store user for later access
    # ---------- cross-field validation ----------
    def clean(self):
        """
        Perform cross-field validation: check credentials.
        """
        cleaned = super().clean()
        username = cleaned.get("username")
        password = cleaned.get("password")

        if username and password:
            # Use Django's auth backend; returns a User model or None.
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                # General error not tied to a single field.
                raise forms.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            self._user = user  # store for later access

        return cleaned

    # ---------- expose authenticated user ----------
    # After validation, provide access to the authenticated user
    # ---------- expose authenticated user ----------
    def get_user(self):
        """
        Expose the authenticated Django user to the view/service.
        """
        return self._user


# Registration form used by the register_view.
# Validates input and normalizes email.
# Also checks password confirmation and strength.
class RegistrationForm(forms.Form):
    """
    Registration form used by the register_view.
    """

    # ---------- form fields ----------
    # Define all necessary fields with widgets and error messages
    # ---------- form fields ----------
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter First Name"}
        ),        
        max_length=150,       
        error_messages={"required": "First Name is required."},
    )
    middle_name = forms.CharField(
        label="Middle Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Middle Name"}
        ),
        max_length=150,
        error_messages={"required": "Middle Name is required."},
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Last Name"}
        ),
        max_length=150,
        error_messages={"required": "Last Name is required."},
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Email"}
        ),
        error_messages={"required": "Email is required."},
    )
    phone_no = forms.CharField(
        label="Phone No",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Phone No"}
        ),
        max_length=20,
        required=False,
    )
    mobile_no = forms.CharField(
        label="Mobile No",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Mobile No"}
        ),
        max_length=20,
        required=True,
        error_messages={"required": "Mobile No is required."},
    )
    address = forms.CharField(
        label="Address",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Address",
                "rows": 3,  # height in text lines
                "cols": 40,  # width in characters
            }
        ),
        required=False,
    )
    organization = forms.CharField(
        label="Organization",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Organization"}
        ),
        max_length=255,
        required=False,
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        ),
        required=True,
        error_messages={"required": "Password is required."},
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Confirm Password"}
        ),
        required=True,
        error_messages={"required": "Confirm Password is required."},
    )
    terms_accepted = forms.BooleanField(
        label="I accept the terms and conditions",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        required=True,
        error_messages={
            "required": "You must accept the terms and conditions to register."
        },
    )

    # ---------- field-level normalization ----------
    # Normalize email to lowercase
    # ---------- field-level normalization ----------
    def clean_email(self):
        """
        Normalize email to lowercase.
        """
        email = self.cleaned_data["email"].lower()
        return email

    # ---------- cross-field validation ----------
    # Check password confirmation and strength
    # ---------- cross-field validation ----------
    def clean(self):
        """
        Cross-field validation for password confirmation.
        """
        cleaned = super().clean()
        pwd1 = cleaned.get("password1")
        pwd2 = cleaned.get("password2")

        if pwd1 and pwd2 and pwd1 != pwd2:
            self.add_error("password2", "Passwords do not match.")

        if pwd1:
            # Use Django's built-in password validators.
            password_validation.validate_password(pwd1)

        return cleaned


# Password reset request form.
# Used to initiate password reset by email.
class PasswordResetRequestForm(forms.Form):
    """
    First step: user submits their email.
    """

    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Email is required.",
        },
    )


# Password reset confirmation form.
# Used to set a new password after clicking the reset link.
# Inherits Django's SetPasswordForm for strong validation.
# The view will handle UserId decoding and token validation.
# The form just sets the new password.
class PasswordResetConfirmForm(DjangoSetPasswordForm):
    """
    Second step: user chooses a new password.

    Inherits Django's SetPasswordForm so you get strong validation.
    """

    # no extra fields; just reuse constructor/cleaning
    pass
