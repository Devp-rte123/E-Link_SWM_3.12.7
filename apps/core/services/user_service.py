"""
Domain service for user-related use cases.

This layer orchestrates business rules and uses repositories.
"""

# Import future annotations for forward references.
from __future__ import annotations

# Imported dataclass for simple service definition.
from dataclasses import dataclass
# Included for type hints. (For login and registration forms.)
from typing import Optional

# Import domain entities and repository interfaces.
# Imported User for Registration return type.
# Imported UserId for set_password parameter type.
from apps.core.entities.user import User, UserId
# Imported IUserRepository for dependency inversion.
from apps.core.repositories.interfaces import IUserRepository
# Imported for token generation (if needed in future). For password resets.
from django.contrib.auth.tokens import default_token_generator


@dataclass
class UserService:
    """
    High-level user operations for the application.

    Depends only on the IUserRepository abstraction (DIP).
    """
    user_repo: IUserRepository
    
#    ---------- user-related use cases ----------
#   (called by views/forms)
#    ---------- user-related use cases ----------
    def get_user_for_login(self, email: str) -> Optional[User]:
        """
        Domain-level lookup used during login.

        Views/forms deal with credentials; the service exposes
        a simple query in terms of the domain model.
        """
        return self.user_repo.get_by_email(email)

#  ---------- user-related use cases ----------
#   register new user (called by views/forms)
#  ---------- user-related use cases ----------
    def register_user(
        self,
        *,
        first_name: str,
        last_name: str,
        email: str,
        phone_no: str | None,
        mobile_no: str | None,
        address: str | None,
        organization: str | None,
        password: str,
    ) -> User:
        """
        Register a new user if the email is not already taken.
        """
        existing = self.user_repo.get_by_email(email)
        if existing is not None:
            # Domain-level rule: email must be unique.
            raise ValueError("A user with this email already exists.")

        # Delegate persistence details to the repository.
        return self.user_repo.create_user_with_profile(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            mobile_no=mobile_no,
            address=address,
            organization=organization,
            is_active=True,  # or False if you want email activation
        )

#  ---------- user-related use cases ----------
#  change password (called by views/forms)
# ---------- user-related use cases ----------
    def set_password(self, user_id, new_password: str) -> None:
        """
        Change a user's password using the repository.
        """
        self.user_repo.set_password(user_id, new_password)

#  ---------- user-related use cases ----------
#  start password reset (called by views/forms)
# ---------- user-related use cases ----------      
def start_password_reset(self, email: str) -> tuple[str, str] | None:
        """
        Start password reset.

        Returns (UserId, token) for building the email link,
        or None if no user with that email exists.
        """
        user = self.user_repo.get_by_email(email)
        if user is None:
            # Silently ignore unknown emails for security.
            return None

        # Let repository give back the ORM user (or encode id yourself).
        orm_user = self.user_repo.get_orm_user_by_id(user.id)

        UserId = self.user_repo.encode_user_id(orm_user.pk)
        token = default_token_generator.make_token(orm_user)
        return UserId, token
    
#  ---------- user-related use cases ----------
#  finish password reset (called by views/forms)
# ---------- user-related use cases ----------
def finish_password_reset(
        self, user_id: UserId, new_password: str
    ) -> None:
        """
        Actually update the password after token verification.
        """
        self.user_repo.set_password(user_id, new_password)
