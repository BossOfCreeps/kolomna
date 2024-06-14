from django.urls import path

from events.views import (
    EventListView,
    OrganizationListView,
    OrganizationDetailView,
    EventScheduleAPIView,
    EventScheduleLeftsVisitorsView,
    CalendarView,
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    EventScheduleUpdateView,
    EventScheduleDeleteView,
    EventScheduleCreateView,
    EventSetListView,
    EventSetDetailView,
    EventSetCreateView,
    EventSetUpdateView,
    EventSetDeleteView,
    EventSetBuyView,
    EventSetDeleteFromBasketView,
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
    path("event_schedule/create", EventScheduleCreateView.as_view(), name="event_schedule-create"),
    path("event_schedule/<int:pk>/update", EventScheduleUpdateView.as_view(), name="event_schedule-update"),
    path("event_schedule/<int:pk>/delete", EventScheduleDeleteView.as_view(), name="event_schedule-delete"),
    #
    path("event_set", EventSetListView.as_view(), name="event_set-list"),
    path("event_set/<int:pk>", EventSetDetailView.as_view(), name="event_set-detail"),
    path("event_set/create", EventSetCreateView.as_view(), name="event_set-create"),
    path("event_set/<int:pk>/update", EventSetUpdateView.as_view(), name="event_set-update"),
    path("event_set/<int:pk>/delete", EventSetDeleteView.as_view(), name="event_set-delete"),
    path("event_set/<int:pk>/buy", EventSetBuyView.as_view(), name="event_set-buy"),
    path(
        "event_set/<uuid:set_id>/del_from_basket",
        EventSetDeleteFromBasketView.as_view(),
        name="event_set-del_from_basket",
    ),
    #
]
