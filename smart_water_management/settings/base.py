"""
Base Django settings for Smart Water Management project.

These settings are environment-agnostic; environment-specific overrides
should live in development.py / production.py.

Environment-specific overrides (e.g. production) should import from
this module and adjust only what they need.
"""

# Standard library imports
import os
from pathlib import Path
# Third-party imports
from decouple import config  # Reads values from environment / .env

# Project root (…/smart_water_management)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY: In production use a secure, secret value from environment.
SECRET_KEY = config("SECRET_KEY", default="your-secret-key-here")

# DEBUG should be False in production.
DEBUG = config("DEBUG", default=True, cast=bool)

# Local-only by default; extend for Docker or remote deployments.
# In production, set ALLOWED_HOSTS via environment variable.
# E.g. ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
# (to set multiple, separate by commas)
# Example: ALLOWED_HOSTS=localhost,
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# Application definition
INSTALLED_APPS = [
    # Django contrib apps required by admin/auth/static system.
    # Do not remove unless you know what you're doing.
    # Admin site.
    "django.contrib.admin",
    # Authentication framework.
    "django.contrib.auth",
    # Content types framework (needed by auth).
    "django.contrib.contenttypes",
    # Session framework.
    "django.contrib.sessions",
    # Messaging framework.
    "django.contrib.messages",
    # Static files (CSS, JS, images) handling.
    "django.contrib.staticfiles",
    # Project apps
    # Custom apps for authentication, core functionality, admin console, and public portal.
    # Adjust as needed for your project structure.
    # See apps/ directory for more details.
    # Authentication app for user management.
    "apps.authentication",
    # Core app with main business logic.
    "apps.core",
    # Admin console for administrative tasks.
    "apps.admin_console",
    # Public portal for end-users.
    "apps.public_portal",
]

# Middleware stack processes requests/responses.
# Order matters; some depend on others.
# Security middleware should be first.
# Session and auth middleware are required for user sessions.
# CommonMiddleware handles URL normalization.
# CSRF middleware protects against cross-site request forgery.
# MessageMiddleware enables temporary messages storage.
# Clickjacking protection should be last.
# Adjust as needed for additional middleware.
# See Django docs for details.
# https://docs.djangoproject.com/en/stable/topics/http/middleware/
MIDDLEWARE = [
    # Security-related middleware should remain at the top.
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Root URL configuration module.
# Points to the main urls.py file.
# Adjust if your URL structure is different.
# E.g. if using a different app for main URLs.
# See Django docs for details.
# https://docs.djangoproject.com/en/stable/topics/http/urls/
ROOT_URLCONF = "smart_water_management.urls"

# Template engine configuration.
# Uses DjangoTemplates backend.
# Specifies global templates directory and app directories.
# Configures context processors for templates.
# See Django docs for details.
# https://docs.djangoproject.com/en/stable/topics/templates/
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Global templates directory, used for base.html and shared components.
        "DIRS": [BASE_DIR / "templates"],
        # Also search each app's templates/ directory.
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                # Adds debug flag to templates.
                "django.template.context_processors.debug",
                # Exposes request object as `request` in templates.
                "django.template.context_processors.request",
                # Provides `user` and permissions.
                "django.contrib.auth.context_processors.auth",
                # Provides `messages` for Django messages framework.
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI entry point used by runserver and most production servers.
WSGI_APPLICATION = "smart_water_management.wsgi.application"

# SQLite for local development. Swap ENGINE/NAME for PostgreSQL in prod.
DATABASES = {
    "default": {        
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="smart_water"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="Devp@rte123"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     # Database file path (…/smart_water_management/db.sqlite3).
    #     "NAME": BASE_DIR / "db.sqlite3",
    # }
}

# Sensible default password rules; can be tuned as needed.
AUTH_PASSWORD_VALIDATORS = [
    {
        # Checks similarity to user attributes.
        # Prevents passwords that are too similar to username, email, etc.
        # Helps avoid easy-to-guess passwords.
        "NAME": (
            # Built-in Django validator for user attribute similarity.
            "django.contrib.auth.password_validation."
            # Validator class name.        
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        # Enforces minimum length.
        # Default minimum length is 8 characters.
        # Can be adjusted via OPTIONS.
        # Encourages stronger passwords.
        # Longer passwords are generally more secure.
        # Adjust min_length as needed.
        # E.g. min_length=12 for higher security.
        "NAME": ("django.contrib.auth.password_validation." "MinimumLengthValidator"),        
        "OPTIONS": {"min_length": 8},  # Enforce minimum length of 8.
    },
    {
        # Prevents common passwords.
        # Uses a built-in list of common passwords.
        # Helps avoid easily guessable passwords.
        # Encourages users to choose unique passwords.
        # Important for security.
        "NAME": ("django.contrib.auth.password_validation." "CommonPasswordValidator"),
    },
    {
        # Prevents entirely numeric passwords.
        # Numeric-only passwords are weak.
        # Encourages inclusion of letters/symbols.
        # Improves overall password strength.
        # Important for security.
        # E.g. "12345678" would be rejected.
        # Encourages more complex passwords.
        # Improves account security.
        # Important for protecting user data.
        # Encourages better password practices.
        # Helps mitigate brute-force attacks.
        # Encourages use of mixed character types.     
        "NAME": ("django.contrib.auth.password_validation." "NumericPasswordValidator"),
    },
]

# Internationalization settings.
# Adjust LANGUAGE_CODE and TIME_ZONE as needed.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JS, images) served at /static/ in development.
STATIC_URL = "/static/"
# Additional directories for static files.
# E.g. BASE_DIR / "static" for project-level static files.
# You can add more directories as needed.
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type for models.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Auth-related redirects; use named URL patterns for flexibility.
# Adjust names as per your URL configuration.
LOGIN_URL = "login"
# Redirect to public dashboard after login.
# Adjust as needed.
# E.g. to 'admin_dashboard' for admin users.
LOGIN_REDIRECT_URL = "public_dashboard"
# Redirect to login page after logout.
# Adjust as needed.
# E.g. to 'goodbye' page if desired.
LOGOUT_REDIRECT_URL = "login"

# Email settings (development only), Later you can switch to SMTP or another backend for real emails.
# For development, use console backend to print emails to console.
# In production, configure SMTP or other email backend.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "no-reply@smartwater.local"
