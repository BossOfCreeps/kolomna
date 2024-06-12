from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, TemplateView

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


class EventDetailView(DetailView):
    model = Event


class EventScheduleAPIView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            [
                {"id": s.id, "date_range": s.date_range}
                for s in EventSchedule.objects.filter(
                    event_id=self.request.GET["event_id"], start_at__gte=timezone.now()
                )
            ],
            safe=False,
        )


class EventScheduleLeftsVisitorsView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(EventSchedule.objects.get(pk=self.request.GET["event_schedule_id"]).lefts_visitors)


class CalendarView(TemplateView):
    template_name = "events/calendar.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_schedules"] = EventSchedule.objects.all()
        return context
