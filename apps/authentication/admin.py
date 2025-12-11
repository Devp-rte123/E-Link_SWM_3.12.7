"""
Admin registrations for authentication models.
apps/authentication/admin.py (optional but typical)
"""

from __future__ import annotations

from django.contrib import admin

from apps.authentication.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Basic admin configuration for viewing user profiles.
    """
    list_display = ("user", "phone_no", "mobile_no", "organization", "created_at")
    search_fields = ("user__email", "phone_no", "mobile_no", "organization")
