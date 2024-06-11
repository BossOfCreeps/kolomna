from datetime import datetime

from django.views.generic import ListView, View

from events.models import EventPrice
from helpers import add_deal
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
