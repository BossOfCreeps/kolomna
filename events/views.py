from django.views.generic import ListView

from events.models import Event


class EventListView(ListView):
    model = Event
