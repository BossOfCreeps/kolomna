import json
import logging
from collections import defaultdict
from datetime import timedelta

from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, View, DetailView, CreateView
from qrcode.main import make

from events.models import EventSchedulePrice, EventSet
from helpers import create_yookassa_url, add_deal, update_deal_stage, add_task
from tickets.forms import BuyForm, ReviewForm
from tickets.models import BasketEvent, Purchase, PurchaseEvent, EventPriceCategory, PurchaseStatus
from users.models import CustomUser

logger = logging.getLogger(__name__)


class BasketView(TemplateView):
    template_name = "tickets/basket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        has_collisions, more_then_total_count = False, set()
        date_ranges = []
        total_price, total_count = 0, defaultdict(int)
        set_ids = set()
        data = defaultdict(lambda: defaultdict(list))
        for obj in self.request.user.basket_events.order_by("event_price__event_schedule__start_at").all():
            data[obj.event_price.event_schedule.start_at.date()][obj.event_price.event_schedule].append(obj)

            if obj.count > obj.event_price.max_visitors:
                more_then_total_count.add(obj.id)

            if not has_collisions:
                for range_start, range_end, event_schedule in date_ranges:
                    if event_schedule == obj.event_price.event_schedule:
                        continue

                    event_schedule_start = obj.event_price.event_schedule.start_at - timedelta(minutes=45)
                    event_schedule_end = obj.event_price.event_schedule.end_at + timedelta(minutes=45)

                    if (
                        range_start < event_schedule_start < range_end
                        or range_start < event_schedule_end < range_end
                        or (range_start < event_schedule_start and range_end > event_schedule_end)
                        or (range_start > event_schedule_start and range_end < event_schedule_end)
                    ):
                        has_collisions = True
                        break

            date_ranges.append(
                [
                    obj.event_price.event_schedule.start_at,
                    obj.event_price.event_schedule.end_at,
                    obj.event_price.event_schedule,
                ]
            )

            if obj.set_id is None:
                total_price += obj.count * obj.event_price.price
            elif obj.set_id not in set_ids:
                set_ids.add(obj.set_id)
                total_price += EventSet.objects.get(set_id=obj.set_id).price

            total_count[obj.event_price.event_schedule] += obj.count

        data_copy = {}
        for k, v in data.items():
            data_copy[k] = dict(v)

        context["data"] = data_copy
        context["total_price"] = total_price
        context["users"] = CustomUser.objects.filter(is_tic_employee=False)

        context["sets"] = EventSet.objects.filter(set_id__in=set_ids)

        context["has_collisions"] = has_collisions

        for es, count in total_count.items():
            if count > es.event.max_visitors:
                for be in BasketEvent.objects.filter(event_price_id__in=es.prices.values_list("id", flat=True)):
                    more_then_total_count.add(be.id)

        context["more_then_total_count"] = more_then_total_count

        return context


class BuyBasketView(View):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        by_tic_employee = "user" in self.request.POST
        user_id = self.request.POST.get("user") if by_tic_employee else request.user.id

        qs = BasketEvent.objects.filter(user=request.user)

        singles_basket_events = []
        sets_basket_events = defaultdict(list)
        for obj in qs:
            if obj.set_id is None:
                singles_basket_events.append([obj])
            else:
                sets_basket_events[obj.set_id].append(obj)

        purchase_ids, mega_total_price = [], 0
        for basket_events in singles_basket_events + list(sets_basket_events.values()):
            purchase = Purchase.objects.create(user_id=user_id, total_price=0)

            total_price, objs, set_id = 0, [], None
            for obj in basket_events:
                set_id = obj.set_id
                if set_id is None:
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

            if set_id is not None:
                total_price = EventSet.objects.get(set_id=set_id).price

            purchase.total_price = total_price
            purchase.set_id = set_id
            purchase_ids.append(purchase.id)

            mega_total_price += total_price

            purchase.bitrix_id = add_deal(
                purchase.title, purchase.user.bitrix_id, total_price, basket_events, is_set=set_id is not None
            )

            purchase.save()
            BasketEvent.objects.filter(user=request.user).delete()

        if by_tic_employee:
            for bitrix_id in Purchase.objects.filter(id__in=purchase_ids).values_list("bitrix_id", flat=True):
                update_deal_stage(bitrix_id)
            return redirect(reverse("tickets:basket"))

        yookassa_url = create_yookassa_url(
            mega_total_price,
            purchase_ids,
            request.user,
            f'{self.request.scheme}://{self.request.get_host()}{reverse("users:profile")}',
        )

        Purchase.objects.filter(id__in=purchase_ids).update(yookassa_url=yookassa_url)

        return redirect(yookassa_url)


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
        BasketEvent.objects.filter(event_price__event_schedule_id=self.kwargs["pk"], set_id__isnull=True).delete()
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

        logging.debug(data)

        qs = Purchase.objects.filter(yookassa_url__endswith=data["object"]["id"])

        if data["event"] == "payment.succeeded":
            for purchase in qs:
                purchase.status = PurchaseStatus.SUCCESS.value
                update_deal_stage(purchase.bitrix_id)
                add_task(f"Позвонить по: {purchase.title}", purchase.bitrix_id)
                purchase.save()

        elif data["event"] == "payment.canceled":
            qs.update(status=PurchaseStatus.CLOSED.value)

        return HttpResponse()


class PurchaseReviewView(CreateView):
    form_class = ReviewForm
    template_name = "tickets/purchase_review.html"

    def get_form_kwargs(self):
        kwargs = super(PurchaseReviewView, self).get_form_kwargs()
        kwargs["purchases"] = (
            Purchase.objects.filter(pk=self.request.GET["id"]) if self.request.GET.get("id") else Purchase.objects.all()
        )
        return kwargs
