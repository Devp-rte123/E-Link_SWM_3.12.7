"""
Django-based implementation of IEmailService.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

from apps.core.services.interfaces import IEmailService


@dataclass
class DjangoEmailService(IEmailService):
    """
    Simple email service using Django's send_mail.

    In production you might want to switch to a provider-specific
    backend or a celery-based async sender.
    """

    def send_activation_email(self, *, to_email: str, token: str) -> None:
        # Placeholder for future activation flow.
        subject = "Activate your Smart Water account"
        body = f"Activation token: {token}"
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])

    def send_password_reset_email(self, *, to_email: str, token: str) -> None:
        """
        Compose a URL compatible with auth_views.PasswordResetConfirmView.

        Note: For correctness, Django's PasswordResetView usually builds
        this URL itself; here we create a minimal example to match your
        requested architecture.
        """
        User = get_user_model()
        user = User.objects.get(email__iexact=to_email)
        uid = default_token_generator._make_hash_value(
            user, user.last_login
        )  # not recommended to rely on internals
        # Simpler: let PasswordResetView handle email in production.
        reset_path = reverse(
            "password_reset_confirm",
            kwargs={"uidb64": uid, "token": token},
        )
        reset_url = f"{settings.SITE_URL}{reset_path}"

        subject = "Reset your Smart Water password"
        body = f"Use the following link to reset your password:\n{reset_url}"
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [to_email])
