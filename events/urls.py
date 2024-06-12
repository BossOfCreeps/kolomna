from django.urls import path

from events.views import (
    EventListView,
    OrganizationListView,
    OrganizationDetailView,
    EventScheduleAPIView,
    EventScheduleLeftsVisitorsView,
)

app_name = "events"

urlpatterns = [
    path("organisations", OrganizationListView.as_view(), name="organisation-list"),
    path("organisations/<int:pk>", OrganizationDetailView.as_view(), name="organisation-detail"),  # TODO:
    path("", EventListView.as_view(), name="event-list"),
    path("api/event_schedule", EventScheduleAPIView.as_view(), name="event_schedule-list"),
    path(
        "api/event_schedule/left_visitors",
        EventScheduleLeftsVisitorsView.as_view(),
        name="event_schedule-left_visitors",
    ),
]
