from django.conf import settings
from django.views.generic import ListView, DetailView

from events.filters import EventFilter
from events.models import Event, Organization, EventPriceCategory


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class EventListView(ListView):
    model = Event
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        return EventFilter(self.request.GET, Event.objects.all()).qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizations"] = Organization.objects.all()
        context["categories"] = EventPriceCategory.choices

        event_filter = EventFilter(self.request.GET, Event.objects.all())
        event_filter.is_valid()
        context["form_data"] = event_filter.form.cleaned_data

        return context
