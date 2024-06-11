from django.urls import path

from events.views import EventListView

app_name = "events"

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
]
