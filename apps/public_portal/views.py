"""
Views for end-user dashboards and public portal pages.
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def base_shell_view(request: HttpRequest) -> HttpResponse:
    """
    Render the bare base.html layout without extra content blocks.
    Useful as a landing page or for quickly testing the layout.
    """
    return render(request, "base.html")

@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Render the public (normal) user dashboard.

    The KPI values are static placeholders for now and are intended to
    be replaced by dynamic data coming from services / repositories.
    """
    context = {
        # Example: water usage for the current day in litres.
        "contractors_count": 120,
        # Example: total usage in the current month.
        "employees_count": 1000,
        # Example: number of alerts / anomalies detected today.
        "meter_replacement_count": 20,
    }
    return render(request, "public_portal/dashboard.html", context)