from django.urls import path

from events.views import (
    EventListView,
    OrganizationListView,
    OrganizationDetailView,
    EventScheduleAPIView,
    EventScheduleLeftsVisitorsView,
    CalendarView,
    EventDetailView,
    EventScheduleDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventScheduleUpdateView,
    EventScheduleDeleteView,
    EventScheduleCreateView,
)

app_name = "events"

urlpatterns = [
    path("organisations", OrganizationListView.as_view(), name="organisation-list"),
    path("organisations/<int:pk>", OrganizationDetailView.as_view(), name="organisation-detail"),  # TODO:
    #
    path("", EventListView.as_view(), name="event-list"),
    path("<int:pk>", EventDetailView.as_view(), name="event-detail"),
    path("create", EventCreateView.as_view(), name="event-create"),
    path("<int:pk>/update", EventUpdateView.as_view(), name="event-update"),
    path("<int:pk>/delete", EventDeleteView.as_view(), name="event-delete"),
    #
    path("api/event_schedule", EventScheduleAPIView.as_view(), name="event_schedule-list"),
    path(
        "api/event_schedule/left_visitors",
        EventScheduleLeftsVisitorsView.as_view(),
        name="event_schedule-left_visitors",
    ),
    #
    path("calendar", CalendarView.as_view(), name="calendar"),
    #
    path("event_schedule/<int:pk>", EventScheduleDetailView.as_view(), name="event_schedule-detail"),
    path("event_schedule/create", EventScheduleCreateView.as_view(), name="event_schedule-create"),
    path("event_schedule/<int:pk>/update", EventScheduleUpdateView.as_view(), name="event_schedule-update"),
    path("event_schedule/<int:pk>/delete", EventScheduleDeleteView.as_view(), name="event_schedule-delete"),
    #
]
