from datetime import datetime

import django_filters
from django.db.models import Q

from events.models import Event, Organization, EventPrice, EventSchedule


class EventFilter(django_filters.FilterSet):
    organization = django_filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    duration_gte = django_filters.NumberFilter(field_name="duration", lookup_expr="gte")
    duration_lte = django_filters.NumberFilter(field_name="duration", lookup_expr="lte")

    max_visitors_standard = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_child = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_student = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_retiree = django_filters.NumberFilter(method="max_visitors_filter")

    max_price_standard = django_filters.NumberFilter(method="max_price_filter")
    max_price_child = django_filters.NumberFilter(method="max_price_filter")
    max_price_student = django_filters.NumberFilter(method="max_price_filter")
    max_price_retiree = django_filters.NumberFilter(method="max_price_filter")

    date = django_filters.DateFilter(method="datetime_filter")
    time_gte = django_filters.TimeFilter(method="datetime_filter")
    time_lte = django_filters.TimeFilter(method="datetime_filter")

    @staticmethod
    def max_visitors_filter(queryset, name, value):
        return queryset.filter(
            pk__in=EventPrice.objects.filter(category=name.split("_")[-1].upper(), max_visitors__gte=value).values_list(
                "event", flat=True
            )
        )

    @staticmethod
    def max_price_filter(queryset, name, value):
        return queryset.filter(
            pk__in=EventPrice.objects.filter(category=name.split("_")[-1].upper(), price__lte=value).values_list(
                "event", flat=True
            )
        )

    datetime_filter_skip = False

    def datetime_filter(self, queryset, _, __):
        if self.datetime_filter_skip:
            return queryset

        self.datetime_filter_skip = True

        qs = EventSchedule.objects

        if self.form.cleaned_data.get("date") is not None:
            v = self.form.cleaned_data["date"]
            qs = qs.filter(
                start_at__lte=datetime.combine(v, datetime.max.time()),
                end_at__gte=datetime.combine(v, datetime.min.time()),
            )

        if self.form.cleaned_data.get("time_gte") is not None:
            v = self.form.cleaned_data["time_gte"]
            qs = qs.filter(Q(start_at__hour__gte=v.hour) | Q(start_at__hour=v.hour, start_at__minute__gte=v.minute))

        if self.form.cleaned_data.get("time_lte") is not None:
            v = self.form.cleaned_data["time_lte"]
            qs = qs.filter(Q(end_at__hour__lte=v.hour) | Q(end_at__hour=v.hour, end_at__hour__lte=v.minute))

        return queryset.filter(pk__in=qs.values_list("event", flat=True))

    class Meta:
        model = Event
        fields = ["organization"]
