"""
Django ORM models for the authentication app.

These classes represent database tables only.
They do NOT contain business rules – those live in the domain layer.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """
    Extra per-user data that is not part of the core auth user table.
    """

    # Link to Django's user model (can be custom).
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="userprofile",
    )

    # Optional profile fields (can be adapted for your project).
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # audit field
    updated_at = models.DateTimeField(auto_now=True)      # audit field

    def __str__(self) -> str:
        """
        Human-readable representation used in admin and shell.
        """
        return f"Profile<{self.user_id}>"