"""
Views for the Smart Water Management admin console.

These provide system-level KPIs and a high-level overview for
administrative users.
"""

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@staff_member_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    Render the admin dashboard.

    Only staff users can access this view (enforced by the decorator).
    The metrics are example values; real implementations should fetch
    data from dedicated services or reporting pipelines.
    """
    context = {
        "total_users": 42,
        "sensors_online": 18,
        "water_sources_online": 4,
        "alerts_today": 3,
    }
    return render(request, "admin_console/dashboard.html", context)