"""
Django ORM implementation of IUserRepository.

This module is infrastructure: it knows about Django and the database,
and maps Django models to domain entities.
"""

# Import future annotations for forward references.
from __future__ import annotations

# Import Optional for return type hints.
from typing import Optional

# Import Django auth utilities.
# Imported get_user_model to access the user model.
from django.contrib.auth import get_user_model
# Imported make_password for secure password hashing.
from django.contrib.auth.hashers import make_password
# Imported for URL-safe base64 encoding of user ids.
from django.utils.http import urlsafe_base64_encode
# Imported for byte conversion.
from django.utils.encoding import force_bytes

# Import domain entities and repository interface.
# Imported UserProfileModel for profile data.
from apps.authentication.models import UserProfile as UserProfileModel  # ORM model
# Imported User, UserId, UserProfile for domain entities.
from apps.core.entities.user import User, UserId, UserProfile          # domain entities
# Imported IUserRepository for implementation.
from apps.core.repositories.interfaces import IUserRepository

# Concrete Django user model class (AUTH_USER_MODEL)
UserModel = get_user_model()

# ---------- UserRepository implementation ----------
#  Persists users using Django ORM.
# ---------- UserRepository implementation ----------
class UserRepository(IUserRepository):
    """
    Concrete repository that persists users using Django ORM.
    """

# ---------- internal mapping helpers ----------
#  Convert Django ORM user + profile to domain User entity
#  Used internally to map ORM models to domain entities
# ---------- internal mapping helpers ----------
    def _to_entity(self, user: UserModel) -> User:
        """
        Convert a Django user instance (and optional profile) to a domain User.
        """
        # ---------- internal mapping helpers ----------
        # Load profile if it exists
        # Map to domain UserProfile entity
        # If no profile, set to None
        # Return domain User entity with profile
        # ---------- internal mapping helpers ----------
        profile_entity: Optional[UserProfile] = None

        try:
            # Load related profile if it exists
            # OneToOne relationship
            # May raise DoesNotExist
            # If no profile, handle exception            
            profile: UserProfileModel = user.userprofile
        except UserProfileModel.DoesNotExist:
            profile = None

        if profile is not None:
            profile_entity = UserProfile(
                id=profile.id,
                user_id=UserId(user.id),
                phone_no=profile.phone_no,
                mobile_no=profile.mobile_no,
                address=profile.address,
                organization=profile.organization,
            )
#  ---------- internal mapping helpers ----------
# Return domain User entity with profile
# ---------- internal mapping helpers ----------
        return User(
            id=UserId(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            date_joined=user.date_joined,
            profile=profile_entity,
        )

# ---------- IUserRepository API ----------
# Load user by email
# Return None if not found
# Used during login
# Used by UserService
# ---------- IUserRepository API ----------
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve user by email (case-insensitive).
        """
        try:
            user = UserModel.objects.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None
        return self._to_entity(user)

# ---------- IUserRepository API ----------
# Load user by id
# Return None if not found
# Used in various user-related operations
# Used by UserService  
# --------- IUserRepository API ----------
    def get_by_id(self, user_id: UserId) -> Optional[User]:
        """
        Retrieve user by domain user id.
        """
        try:
            user = UserModel.objects.get(id=user_id.value)
        except UserModel.DoesNotExist:
            return None
        return self._to_entity(user)

# ---------- IUserRepository API ----------
# Load the Django ORM user instance by domain user id
# Return None if not found
# Used for operations needing the ORM user
# Used by UserRepository implementation
# ---------- IUserRepository API ----------
    def get_orm_user_by_id(self, user_id: UserId):
        """
        Return the raw Django user model for infrastructure tasks.
        """
        return UserModel.objects.get(id=user_id.value)

# ---------- IUserRepository API ----------
# Encode user id to URL-safe base64 string
# Used for generating tokens/links
# Used by UserService implementation
# ---------- IUserRepository API ----------
    def encode_user_id(self, pk: int) -> str:
        """
        Encode primary key to UserId/uidb64 used in reset links.
        """
        return urlsafe_base64_encode(force_bytes(pk))
    
# ---------- IUserRepository API ----------
# Load the Django ORM user instance by domain user id
# Return None if not found
# Used for operations needing the ORM user
# Used by UserRepository implementation
# ---------- IUserRepository API ----------
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
        Create user + profile in one unit of work, returning a domain User.
        """
        user = UserModel.objects.create(
            email=email.lower(),
            username=email.lower(),  # email-as-username
            first_name=first_name,
            last_name=last_name,
            password=make_password(password),  # secure hash
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        UserProfileModel.objects.create(
            user=user,
            phone_no=phone_no,
            mobile_no=mobile_no,
            address=address,
            organization=organization,
        )

        return self._to_entity(user)

# ---------- IUserRepository API ----------
# Encode user id to URL-safe base64 string
# Used for generating tokens/links 
# Used by UserService implementation
# ---------- IUserRepository API ----------
    def set_password(self, user_id: UserId, raw_password: str) -> None:
        """
        Update the user's password with Django's hashing API.
        """
        user = UserModel.objects.get(id=user_id.value)
        user.set_password(raw_password)
        user.save(update_fields=["password"])
