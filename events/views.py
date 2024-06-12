from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from events.filters import EventFilter
from events.models import Event, Organization, EventPriceCategory, EventSchedule


class OrganizationListView(ListView):
    model = Organization


class OrganizationDetailView(DetailView):
    model = Organization


class EventListView(ListView):
    model = Event

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


class EventScheduleAPIView(View):
    def get(self, request, *args, **kwargs):
        # TODO: добавить проверки на остаток
        return JsonResponse(
            [
                {"id": s.id, "date_range": s.date_range}
                for s in EventSchedule.objects.filter(
                    event_id=self.request.GET["event_id"], start_at__gte=timezone.now()
                )
            ],
            safe=False,
        )
