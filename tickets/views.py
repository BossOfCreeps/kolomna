from collections import defaultdict

from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View

from events.models import EventPrice
from tickets.forms import BuyForm
from tickets.models import BasketEvent, EventSchedule, Purchase, PurchaseEvent


class BasketView(TemplateView):
    template_name = "tickets/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_price = 0
        data = defaultdict(lambda: defaultdict(list))
        for obj in self.request.user.basket_events.order_by("event_schedule__start_at").all():
            data[obj.event_schedule.start_at.date()][obj.event_schedule].append(obj)
            all_price += obj.count * obj.event_price.price

        data_copy = {}
        for k, v in data.items():
            data_copy[k] = dict(v)

        context["data"] = data_copy
        context["all_price"] = all_price

        return context


class BuyBasketView(View):
    def post(self, request, *args, **kwargs):
        qs = BasketEvent.objects.filter(user=self.request.user)

        event_prices = EventPrice.objects.filter(pk__in=qs.values_list("event_price", flat=True))
        event_schedules = EventSchedule.objects.filter(pk__in=qs.values_list("event_schedule", flat=True))

        with transaction.atomic():
            purchase = Purchase.objects.create(user=request.user)
            PurchaseEvent.objects.bulk_create(
                [
                    PurchaseEvent(
                        purchase=purchase,
                        event=obj.event_schedule.event,
                        count=obj.count,
                        category=obj.event_price.category,
                        price=obj.event_price.price,
                        start_at=obj.event_schedule.start_at,
                        end_at=obj.event_schedule.end_at,
                    )
                    for obj in qs
                ]
            )

            # TODO: add_deal(
            #    "Заказ",
            #    request.user.bitrix_id,
            #    100,
            #    datetime(2024, 6, 11),
            #    datetime(2024, 6, 12),
            #    event_prices,
            # )

            qs.delete()

        return redirect(reverse("tickets:basket"))


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

        if "next_basket" in request.POST:
            return redirect(reverse("tickets:basket"))

        return redirect(form.cleaned_data["next"])
