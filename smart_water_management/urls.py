"""
Root URL configuration.

This file wires project-level paths to app-level urls.py files.
"""

# Import future annotations for forward references.
from __future__ import annotations

# Imported admin for admin site URLs.
from django.contrib import admin
# Imported include and path for URL pattern definitions.
from django.urls import include, path
# Imported base shell view for root path.
from apps.public_portal.views import base_shell_view

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),
    # Delegate /auth/* URLs to the authentication app.
    path("auth/", include("apps.authentication.urls")),
    # Root path can be delegated to a base shell view or another app.
    path("", base_shell_view, name="root_base"),
    # Delegate other public portal URLs.
    path("", include("apps.public_portal.urls")),
]
