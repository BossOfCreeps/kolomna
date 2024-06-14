from datetime import timedelta

from django.utils import timezone
from django.views.generic import TemplateView

from events.models import EventSchedule, Organization
from cafes.models import Cafe


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: весь день
        context["event_schedules"] = EventSchedule.objects.filter(
            start_at__gte=timezone.now() + timedelta(hours=3)
        ).order_by("start_at")[:3]
        context["organizations"] = Organization.objects.all()[:4]
        context["cafes"] = Cafe.objects.all()[:2]
        return context
