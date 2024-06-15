import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from pprint import pprint

from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView, UpdateView, FormView, DeleteView

from events.filters import EventFilter
from events.forms import EventForm, EventScheduleCreateForm, EventScheduleUpdateForm
from events.models import Event, Organization, EventPriceCategory, EventSchedule, EventSchedulePrice, EventSet
from helpers import add_product
from tickets.models import BasketEvent, PurchaseEvent


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_events"] = Event.objects.filter(~Q(id=self.kwargs["pk"]))
        return context


class EventScheduleAPIView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            [
                {"id": s.id, "date_range": s.date_range}
                for s in EventSchedule.objects.filter(
                    event_id=self.request.GET["event_id"], start_at__gte=timezone.now() + timedelta(hours=3)
                ).order_by("start_at")
            ],
            safe=False,
        )


class EventScheduleLeftsVisitorsView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(EventSchedule.objects.get(pk=self.request.GET["event_schedule_id"]).lefts_visitors_by_cat)


class CalendarView(TemplateView):
    template_name = "events/calendar.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organizations"] = context["all_organizations"] = Organization.objects.all()
        context["event_schedules"] = EventSchedule.objects.all()

        organizations_ids = self.request.GET.getlist("organization")
        if organizations_ids:
            context["organizations"] = Organization.objects.filter(pk__in=organizations_ids)
            context["event_schedules"] = context["event_schedules"].filter(event__organization_id__in=organizations_ids)

        fullness = self.request.GET.getlist("fullness")
        if fullness:
            context["fullness"] = fullness

            ids = []
            for event_schedule in context["event_schedules"]:
                f = event_schedule.all_purchased / event_schedule.event.max_visitors * 100
                if (
                    ("1" in fullness and f < 25)
                    or ("2" in fullness and 25 <= f < 50)
                    or ("3" in fullness and 50 <= f < 75)
                    or ("4" in fullness and 75 <= f)
                ):
                    ids.append(event_schedule.id)

            context["event_schedules"] = context["event_schedules"].filter(id__in=ids)

        return context


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm

    def get_success_url(self):
        return reverse("events:event_schedule-create") + f"?event_id={self.object.id}"


class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm


class EventDeleteView(DeleteView):
    pass


class EventScheduleCreateView(FormView):
    form_class = EventScheduleCreateForm
    template_name = "events/eventschedule_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = (
            Event.objects.filter(pk=self.request.GET["event_id"])
            if self.request.GET.get("event_id")
            else Event.objects.all()
        )
        return context

    @transaction.atomic()
    def form_valid(self, form):
        event = Event.objects.get(pk=form.cleaned_data["event_id"])

        if form.cleaned_data["period"] == "single":
            event_schedule = EventSchedule.objects.create(
                event=event,
                group_id=None,
                start_at=form.cleaned_data["datetime_start"],
                end_at=form.cleaned_data["datetime_end"],
            )
            for cat in EventPriceCategory.values:
                EventSchedulePrice.objects.create(
                    event_schedule=event_schedule,
                    price=form.cleaned_data[f"price_{cat.lower()}"],
                    category=cat,
                    max_visitors=form.cleaned_data[f"visitors_{cat.lower()}"],
                    bitrix_id=add_product(f'"{event.name}" для категории "{cat}"'),
                )

        elif form.cleaned_data["period"] == "periodical":
            group_id = uuid.uuid4()
            cur_date = form.cleaned_data["date_start"] - timezone.timedelta(days=1)

            for _ in range((form.cleaned_data["date_end"] - form.cleaned_data["date_start"]).days + 1):
                cur_date += timezone.timedelta(days=1)

                if form.cleaned_data["weekday"] and str(cur_date.weekday()) not in form.cleaned_data["weekday"]:
                    continue

                event_schedule = EventSchedule.objects.create(
                    event=event,
                    group_id=group_id,
                    start_at=datetime.combine(cur_date, form.cleaned_data["time_start"]),
                    end_at=datetime.combine(cur_date, form.cleaned_data["time_end"]),
                )
                for cat in EventPriceCategory.values:
                    EventSchedulePrice.objects.create(
                        event_schedule=event_schedule,
                        price=form.cleaned_data[f"price_{cat.lower()}"],
                        category=cat,
                        max_visitors=form.cleaned_data[f"visitors_{cat.lower()}"],
                        bitrix_id=add_product(f'"{event.name}" для категории "{cat}"'),
                    )

        return redirect(reverse("events:calendar"))

    def form_invalid(self, form):
        raise Exception(form.errors)


class EventScheduleDetailView(FormView):
    template_name = "events/eventschedule_detail.html"
    form_class = EventScheduleUpdateForm

    def get_context_data(self, **kwargs):
        obj = EventSchedule.objects.get(pk=self.kwargs["pk"])

        context = super().get_context_data(**kwargs)
        context["object"] = obj

        purchase_events = defaultdict(list)
        for pe in PurchaseEvent.objects.filter(event=obj.event, start_at=obj.start_at, end_at=obj.end_at):
            purchase_events[pe.purchase].append(pe)

        context["purchase_events"] = dict(purchase_events)
        return context


class EventSetListView(ListView):
    model = EventSet


class EventSetDetailView(DetailView):
    model = EventSet


class EventSetCreateView(CreateView):
    model = EventSet
    fields = "__all__"


class EventSetUpdateView(UpdateView):
    model = EventSet
    fields = "__all__"


class EventSetDeleteView(DeleteView):
    model = EventSet

    def get_success_url(self):
        return reverse("events:event_set-list")


class EventSetBuyView(View):
    def post(self, request, *args, **kwargs):
        set_id = EventSet.objects.get(pk=self.kwargs["pk"]).set_id

        BasketEvent.objects.bulk_create(
            [
                BasketEvent(
                    event_price=EventSchedulePrice.objects.get(
                        event_schedule_id=v, category=EventPriceCategory.STANDARD.value
                    ),
                    user=request.user,
                    count=1,
                    set_id=set_id,
                )
                for v in self.request.POST.values()
            ]
        )
        return redirect(reverse("tickets:basket"))


class EventSetDeleteFromBasketView(View):
    def get(self, request, *args, **kwargs):
        BasketEvent.objects.filter(set_id=self.kwargs["set_id"]).delete()
        return redirect(reverse("tickets:basket"))
