from django.urls import path

from events.views import EventListView, OrganizationListView, OrganizationDetailView

app_name = "events"

urlpatterns = [
    path("organisations", OrganizationListView.as_view(), name="organisation-list"),
    path("organisations/<int:pk>", OrganizationDetailView.as_view(), name="organisation-detail"),
    path("events", EventListView.as_view(), name="event-list"),
]
