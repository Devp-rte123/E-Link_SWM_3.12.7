"""URL routes for admin dashboard and management views."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="admin_dashboard"),
]