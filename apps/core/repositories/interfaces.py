"""
Repository interfaces for the core domain.

These abstractions decouple domain services from persistence details.
"""

# Import future annotations for forward references.
from __future__ import annotations

# Import ABC and abstractmethod for defining interfaces.
from abc import ABC, abstractmethod
# Imported Optional for return type hints.
from typing import Optional

# Import domain entities for method signatures.
# Imported User for return types.
# Imported UserId for parameter types.
from apps.core.entities.user import User, UserId


# ---------- IUserRepository interface ----------
#  Abstraction for user persistence.
# Domain services depend on this interface, not on Django ORM directly.
# ---------- IUserRepository interface ----------
class IUserRepository(ABC):
    """
    Abstraction for user persistence.

    Domain services depend on this interface, not on Django ORM directly.
    """

#  ---------- IUserRepository API ----------
# Methods for loading/saving users as domain entities.

# ---------- IUserRepository API ----------   
    # Load user by email
    # Return None if not found
    # Used during login
    # Used by UserService
# ---------- IUserRepository API ----------
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Load a user (as a domain entity) by email, or return None if not found.
        """
        raise NotImplementedError
    
# ---------- IUserRepository API ----------   
#  Load user by id
# Return None if not found
# Used in various user-related operations
# Used by UserService
# ---------- IUserRepository API ----------   
    @abstractmethod
    def get_by_id(self, user_id: UserId) -> Optional[User]:
        """
        Load a user by domain user id, or return None if not found.
        """
        raise NotImplementedError
    
# ---------- IUserRepository API ----------     
    # Load the Django ORM user instance by domain user id
    # Return None if not found
    # Used for operations needing the ORM user
    # Used by UserRepository implementation
# ---------- IUserRepository API ----------  
    @abstractmethod
    def get_orm_user_by_id(self, user_id: UserId):
        """
        Load the Django ORM user instance by domain user id, or return None if not found.
        """
        raise NotImplementedError
        
# ---------- IUserRepository API ----------
    # Encode user id to URL-safe base64 string
    # Used for generating tokens/links
    # Used by UserService implementation
# ---------- IUserRepository API ----------
    @abstractmethod
    def encode_user_id(self, pk: int) -> str:
        """
        Encode the user's primary key into a URL-safe base64 string.
        """
        raise NotImplementedError

# ---------- IUserRepository API ----------
    # Create a new user with profile and return as domain entity
    # Used during registration
    # Used by UserService
# ---------- IUserRepository API ----------
    @abstractmethod
    def create_user_with_profile(
        self,
        *,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone_no: str | None,
        mobile_no: str | None,
        address: str | None,
        organization: str | None,
        is_active: bool = False,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> User:
        """
        Create a new user and associated profile, returning a domain entity.
        """
        raise NotImplementedError

# ---------- IUserRepository API ----------
    # Update the user's password
    # Used during password changes/resets
    # Used by UserService
# ---------- IUserRepository API ----------
    @abstractmethod
    def set_password(self, user_id: UserId, raw_password: str) -> None:
        """
        Update the user's password.
        """
        raise NotImplementedError