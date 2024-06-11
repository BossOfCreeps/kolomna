from django.conf import settings
from django.views.generic import ListView, DetailView

from events.models import Event, Organization


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class EventListView(ListView):
    model = Event
    paginate_by = settings.PAGINATE_BY
