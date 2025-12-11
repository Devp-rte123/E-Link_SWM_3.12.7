"""URL routes for public user dashboards and related views."""

from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="public_dashboard"),
]