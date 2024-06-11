from datetime import datetime

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, View

from events.models import EventPrice
from helpers import add_deal
from tickets.forms import BuyForm
from tickets.models import BasketEvent, EventSchedule


class BasketView(ListView):
    model = BasketEvent


class BuyBasketView(View):
    def post(self, request, *args, **kwargs):
        event_prices = EventPrice.objects.filter(
            pk__in=self.request.user.basket_events.values_list("event_price", flat=True)
        )
        event_schedules = EventSchedule.objects.filter(
            pk__in=self.request.user.basket_events.values_list("event_schedule", flat=True)
        )

        print(event_prices)
        print(request.POST)

        add_deal(
            "Заказ",
            request.user.bitrix_id,
            100,
            datetime(2024, 6, 11),
            datetime(2024, 6, 12),
            event_prices,
        )


class EventBuyView(View):
    def post(self, request, *args, **kwargs):
        form = BuyForm(self.request.POST)
        form.is_valid()
        event_id = form.cleaned_data["event_id"]
        schedule = form.cleaned_data["schedule"]

        BasketEvent.objects.bulk_create(
            [
                BasketEvent(
                    event_price=EventPrice.objects.get(event_id=event_id, category=key.split("_")[-1].upper()),
                    event_schedule_id=schedule,
                    user=request.user,
                    count=form.cleaned_data[key],
                )
                for key in ["visitor_standard", "visitor_child", "visitor_student", "visitor_retiree"]
                if form.cleaned_data[key] > 0
            ]
        )
        return redirect(reverse("core:index"))  # TODO
