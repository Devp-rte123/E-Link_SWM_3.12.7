"""
Simple dependency-injection container for the core domain.

Provides factory functions that wire concrete implementations
(UserRepository) to abstractions (IUserRepository, UserService).
"""

# Import future annotations for forward references.
from __future__ import annotations

# Import lru_cache to create singleton-like instances.
from functools import lru_cache

# Import concrete repository and service implementations.
from apps.core.repositories.django_repository import UserRepository

# Import domain services.
from apps.core.services.user_service import UserService


@lru_cache
def get_user_repository() -> UserRepository:
    """
    Return a singleton UserRepository instance.

    Using @lru_cache keeps one instance per process,
    which is sufficient for typical Django apps.
    """
    return UserRepository()


@lru_cache
def get_user_service() -> UserService:
    """
    Return a singleton UserService wired with UserRepository.

    Views call this instead of constructing UserService directly.
    """
    return UserService(user_repo=get_user_repository())
