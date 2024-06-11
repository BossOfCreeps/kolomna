from datetime import datetime

import django_filters

from events.models import Event, Organization, EventPrice, EventSchedule


class EventFilter(django_filters.FilterSet):
    organization = django_filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    duration_gte = django_filters.NumberFilter(field_name="duration", lookup_expr="gte")
    duration_lte = django_filters.NumberFilter(field_name="duration", lookup_expr="lte")

    max_visitors_standard = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_child = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_student = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_retiree = django_filters.NumberFilter(method="max_visitors_filter")

    date = django_filters.DateFilter(method="date_filter")
    time_gte = django_filters.Filter(method="time_filter")
    time_lte = django_filters.Filter(method="time_filter")

    @staticmethod
    def max_visitors_filter(queryset, name, value):
        return queryset.filter(
            pk__in=EventPrice.objects.filter(category=name.split("_")[-1].upper(), max_visitors__gte=value).values_list(
                "event", flat=True
            )
        )

    def date_filter(self, queryset, _, value):
        print(self.form.cleaned_data)
        return queryset.filter(
            pk__in=EventSchedule.objects.filter(
                start_at__lte=datetime.combine(value, datetime.max.time()),
                end_at__gte=datetime.combine(value, datetime.min.time()),
            ).values_list("event", flat=True)
        )

    def time_filter(self, queryset, _, value):
        print(self.form.cleaned_data)
        return queryset

    class Meta:
        model = Event
        fields = ["organization"]
