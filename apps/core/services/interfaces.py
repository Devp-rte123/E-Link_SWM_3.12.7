"""
Service interfaces for authentication / user flows.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from apps.core.entities.user import User


class IEmailService(ABC):
    """
    Abstraction over Django's email sending facilities.
    """

    @abstractmethod
    def send_activation_email(self, *, to_email: str, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_password_reset_email(self, *, to_email: str, token: str) -> None:
        raise NotImplementedError


class IUserService(ABC):
    """
    Use-case level operations for registration, login, and password reset.
    """

    # -- registration / activation --------------------------------------------

    @abstractmethod
    def register_user(
        self,
        *,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        email: str,
        phone_no: str | None,
        mobile_no: str,
        address: str | None,
        organization: str | None,
        password: str,
    ) -> User:
        """
        Register a new user and return the created entity.

        The implementation may create the user as inactive and send an
        activation email out-of-band.
        """
        raise NotImplementedError

    # -- login / lookup -------------------------------------------------------

    @abstractmethod
    def get_user_for_login(self, email: str) -> Optional[User]:
        """
        Look up an active user by email to be used with Django's
        authenticate() function.
        """
        raise NotImplementedError

    # -- password reset -------------------------------------------------------

    @abstractmethod
    def start_password_reset(self, email: str) -> None:
        """
        Initiate password reset for the given email, if a user exists.

        Implementations should be careful not to leak existence of
        accounts through responses (always behave the same).
        """
        raise NotImplementedError

    @abstractmethod
    def finish_password_reset(self, user: User, new_password: str) -> None:
        """
        Set a new password for the user after token validation succeeds.
        """
        raise NotImplementedError
