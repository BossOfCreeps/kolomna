from collections import defaultdict

from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, DetailView
from qrcode.main import make

from events.models import EventSchedulePrice
from tickets.forms import BuyForm
from tickets.models import BasketEvent, EventSchedule, Purchase, PurchaseEvent, EventPriceCategory


class BasketView(TemplateView):
    template_name = "tickets/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_price = 0
        data = defaultdict(lambda: defaultdict(list))
        for obj in self.request.user.basket_events.order_by("event_price__event_schedule__start_at").all():
            data[obj.event_price.event_schedule.start_at.date()][obj.event_price.event_schedule].append(obj)
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

        with transaction.atomic():
            purchase = Purchase.objects.create(user=request.user)
            PurchaseEvent.objects.bulk_create(
                [
                    PurchaseEvent(
                        purchase=purchase,
                        event=obj.event_price.event_schedule.event,
                        count=obj.count,
                        category=obj.event_price.category,
                        price=obj.event_price.price,
                        start_at=obj.event_price.event_schedule.start_at,
                        end_at=obj.event_price.event_schedule.end_at,
                    )
                    for obj in qs
                ]
            )
            purchase.qr_code.save(f"{purchase.pk}.jpg", ContentFile(""), save=True)
            make(f'{self.request.get_host()}{reverse("tickets:purchase-detail", args=[purchase.pk])}').save(
                purchase.qr_code.path
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

        return redirect(reverse("tickets:purchase-detail", args=[purchase.pk]))


class EventBuyView(View):
    def post(self, request, *args, **kwargs):
        form = BuyForm(self.request.POST)
        form.is_valid()
        schedule = form.cleaned_data["schedule"]

        BasketEvent.objects.bulk_create(
            [
                BasketEvent(
                    event_price=EventSchedulePrice.objects.get(
                        event_schedule=schedule, category=key.split("_")[-1].upper()
                    ),
                    user=request.user,
                    count=form.cleaned_data[f"visitor_{key.lower()}"],
                )
                for key in EventPriceCategory.values
                if form.cleaned_data.get(f"visitor_{key.lower()}")
            ]
        )

        if "next_basket" in request.POST:
            return redirect(reverse("tickets:basket"))

        return redirect(form.cleaned_data["next"])


class EventDeleteView(View):
    def get(self, request, *args, **kwargs):
        EventSchedule.objects.filter(pk=self.kwargs["pk"]).delete()
        return redirect(reverse("tickets:basket"))


class PurchaseDetailView(DetailView):
    model = Purchase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = defaultdict(lambda: defaultdict(list))
        for purchase_event in self.object.events.order_by("start_at").all():
            data[purchase_event.start_at.date()][purchase_event.start_at].append(purchase_event)

        data_copy = {}
        for k, v in data.items():
            data_copy[k] = dict(v)

        context["data"] = data_copy
        return context
