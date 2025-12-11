"""
Domain entities for the user aggregate.

These classes are framework-agnostic and contain only business data/behavior.
They do NOT import Django or use the ORM.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class UserId:
    """
    Strongly-typed user identifier instead of using plain int/UUID everywhere.
    """
    value: int  # or UUID if you use UUID PKs


@dataclass
class UserProfile:
    """
    Domain view of a user's profile data.

    This is separate from the Django ORM model to keep the domain clean.
    """
    id: int
    user_id: UserId
    phone_no: Optional[str]
    mobile_no: Optional[str]
    address: Optional[str]
    organization: Optional[str]


@dataclass
class User:
    """
    Domain entity representing an authenticated user.

    This mirrors only the fields that matter to business logic,
    not necessarily the full Django User model.
    """
    id: UserId
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_staff: bool
    is_superuser: bool
    date_joined: datetime
    profile: Optional[UserProfile] = None

    # Example domain behavior (business rule) – not strictly required:
    def activate(self) -> None:
        """
        Mark the user as active in the domain model.
        Persistence is handled by repositories.
        """
        self.is_active = True