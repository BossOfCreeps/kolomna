import json
from collections import defaultdict

from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, DetailView
from qrcode.main import make

from events.models import EventSchedulePrice
from helpers import create_yookassa_url
from tickets.forms import BuyForm
from tickets.models import BasketEvent, EventSchedule, Purchase, PurchaseEvent, EventPriceCategory, PurchaseStatus
from users.models import CustomUser


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
        context["users"] = CustomUser.objects.filter(is_tic_employee=False)

        return context


class BuyBasketView(View):
    def post(self, request, *args, **kwargs):
        by_tic_employee = "user" in self.request.POST
        user_id = self.request.POST.get("user") if by_tic_employee else request.user.id

        qs = BasketEvent.objects.filter(user=request.user)

        with transaction.atomic():
            purchase = Purchase.objects.create(user_id=user_id, total_price=0)

            total_price, objs = 0, []
            for obj in qs:
                total_price += obj.count * obj.event_price.price
                objs.append(
                    PurchaseEvent(
                        purchase=purchase,
                        event=obj.event_price.event_schedule.event,
                        count=obj.count,
                        category=obj.event_price.category,
                        price=obj.event_price.price,
                        start_at=obj.event_price.event_schedule.start_at,
                        end_at=obj.event_price.event_schedule.end_at,
                    )
                )
            PurchaseEvent.objects.bulk_create(objs)

            purchase.qr_code.save(f"{purchase.pk}.jpg", ContentFile(""), save=True)
            make(f'{self.request.get_host()}{reverse("tickets:purchase-detail", args=[purchase.pk])}').save(
                purchase.qr_code.path
            )

            if by_tic_employee:
                purchase.status = PurchaseStatus.SUCCESS.value
            else:
                purchase.yookassa_url = create_yookassa_url(
                    total_price,
                    purchase.id,
                    request.user,
                    f'{self.request.scheme}://{self.request.get_host()}{reverse("users:profile")}',
                )
            purchase.total_price = total_price
            purchase.save()

            # TODO: add_deal(
            #    "Заказ",
            #    request.user.bitrix_id,
            #    100,
            #    datetime(2024, 6, 11),
            #    datetime(2024, 6, 12),
            #    event_prices,
            # )

            qs.delete()

        if by_tic_employee:
            return redirect(reverse("core:index"))
        else:
            return redirect(purchase.yookassa_url)


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


class PurchaseApproveView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(self.request.body.decode("utf-8"))

        print(data)

        qs = Purchase.objects.filter(yookassa_url__endswith=data["object"]["id"])

        if data["event"] == "payment.succeeded":
            qs.update(status=PurchaseStatus.SUCCESS.value)
        elif data["event"] == "payment.canceled":
            qs.update(status=PurchaseStatus.CLOSED.value)

        return HttpResponse()
