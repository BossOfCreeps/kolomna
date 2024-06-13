from datetime import datetime

import django_filters
from django.db.models import Q

from events.models import Event, Organization, EventSchedulePrice


class EventFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter()
    organization = django_filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())

    duration_gte = django_filters.NumberFilter(field_name="duration", lookup_expr="gte")
    duration_lte = django_filters.NumberFilter(field_name="duration", lookup_expr="lte")

    max_visitors_standard = django_filters.NumberFilter(method="event_schedule_price_filter")
    max_visitors_child = django_filters.NumberFilter(method="event_schedule_price_filter")
    max_visitors_student = django_filters.NumberFilter(method="event_schedule_price_filter")
    max_visitors_retiree = django_filters.NumberFilter(method="event_schedule_price_filter")

    max_price_standard = django_filters.NumberFilter(method="event_schedule_price_filter")
    max_price_child = django_filters.NumberFilter(method="event_schedule_price_filter")
    max_price_student = django_filters.NumberFilter(method="event_schedule_price_filter")
    max_price_retiree = django_filters.NumberFilter(method="event_schedule_price_filter")

    date = django_filters.DateFilter(method="event_schedule_price_filter")
    time_gte = django_filters.TimeFilter(method="event_schedule_price_filter")
    time_lte = django_filters.TimeFilter(method="event_schedule_price_filter")

    event_schedule_price_filter_skip = False

    def event_schedule_price_filter(self, queryset, _, __):
        if self.event_schedule_price_filter_skip:
            return queryset

        self.event_schedule_price_filter_skip = True

        qs = EventSchedulePrice.objects

        for k in ["max_visitors_standard", "max_visitors_child", "max_visitors_student", "max_visitors_retiree"]:
            if self.form.cleaned_data.get(k) is not None:
                qs = qs.filter(category=k.split("_")[-1].upper(), max_visitors__gte=self.form.cleaned_data[k])

        for k in ["max_price_standard",  "max_price_child",  "max_price_student",  "max_price_retiree"]:
            if self.form.cleaned_data.get(k) is not None:
                qs = qs.filter(category=k.split("_")[-1].upper(), price__lte=self.form.cleaned_data[k])

        if self.form.cleaned_data.get("date") is not None:
            v = self.form.cleaned_data["date"]
            qs = qs.filter(
                event_schedule__start_at__lte=datetime.combine(v, datetime.max.time()),
                event_schedule__end_at__gte=datetime.combine(v, datetime.min.time()),
            )

        if self.form.cleaned_data.get("time_gte") is not None:
            v = self.form.cleaned_data["time_gte"]
            qs = qs.filter(
                Q(event_schedule__start_at__hour__gt=v.hour)
                | Q(event_schedule__start_at__hour=v.hour, event_schedule__start_at__minute__gte=v.minute)
            )

        if self.form.cleaned_data.get("time_lte") is not None:
            v = self.form.cleaned_data["time_lte"]
            qs = qs.filter(
                Q(event_schedule__end_at__hour__lt=v.hour)
                | Q(event_schedule__end_at__hour=v.hour, event_schedule__end_at__minute__lte=v.minute)
            )

        return queryset.filter(pk__in=qs.values_list("event_schedule__event", flat=True))

    class Meta:
        model = Event
        fields = ["id", "organization"]
