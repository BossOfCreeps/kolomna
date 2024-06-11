import django_filters

from events.models import Event, Organization, EventPriceCategory, EventPrice


class EventFilter(django_filters.FilterSet):
    organization = django_filters.ModelMultipleChoiceFilter(queryset=Organization.objects.all())
    duration_gte = django_filters.NumberFilter(field_name="duration", lookup_expr="gte")
    duration_lte = django_filters.NumberFilter(field_name="duration", lookup_expr="lte")
    max_visitors_standard = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_child = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_student = django_filters.NumberFilter(method="max_visitors_filter")
    max_visitors_retiree = django_filters.NumberFilter(method="max_visitors_filter")

    @staticmethod
    def max_visitors_filter(queryset, name, value):
        return queryset.filter(
            pk__in=EventPrice.objects.filter(category=name.split("_")[-1].upper(), max_visitors__gte=value).values_list(
                "event", flat=True
            )
        )

    class Meta:
        model = Event
        fields = ["organization"]
