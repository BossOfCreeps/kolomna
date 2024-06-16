import uuid
from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone

from helpers import datetime_to_str, date_to_str


class Organization(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    file = models.ImageField(upload_to="media/organizations", null=True, blank=True)
    address = models.TextField("Адрес")
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")

    color = models.CharField("Цвет", max_length=64)
    short_name = models.CharField("Короткое название", max_length=1024)
    abbreviation = models.CharField("Аббревиатура", max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ["id"]


class Event(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE, "events", verbose_name="Организация")

    name = models.CharField("Название", max_length=1024)
    age_limit = models.CharField("Возрастной ценз", max_length=1024)
    html_description = models.TextField("HTML описание")
    duration = models.PositiveIntegerField("Длительность в минутах")
    max_visitors = models.PositiveIntegerField("Максимальное количество посетителей всего")

    abbreviation = models.CharField("Аббревиатура", max_length=1024)

    @property
    def duration_as_str(self):
        return f"{round(self.duration/60, 1)} часа"

    @property
    def price_range(self):
        obj = EventSchedulePrice.objects.filter(event_schedule__event=self).order_by("price")
        if not obj:
            return "-"

        max_price, min_price = obj.last().price, obj.first().price
        if max_price == min_price:
            return f"{max_price}"

        return f"{min_price}-{max_price}"

    @property
    def active_event_schedules(self):
        return self.schedules.filter(start_at__gte=timezone.now() + timedelta(hours=3))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("events:event-detail", args=[self.id])

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ["id"]


class EventImage(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, "images", verbose_name="Мероприятие")
    file = models.ImageField(upload_to="media/events")

    class Meta:
        ordering = ["id"]


class EventSchedule(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, "schedules", verbose_name="Мероприятие")
    group_id = models.UUIDField("Группа", null=True, blank=True)
    start_at = models.DateTimeField("Дата и время начало")
    end_at = models.DateTimeField("Дата и время конца")

    @property
    def start_at_as_str(self):
        return datetime_to_str(self.start_at + timedelta(hours=3))

    @property
    def end_at_as_str(self):
        return datetime_to_str(self.end_at + timedelta(hours=3))

    @property
    def date_range(self):
        if self.start_at.date() == self.end_at.date():
            return (
                f"{date_to_str(self.start_at.date())} "
                f"{(self.start_at + timedelta(hours=3)).strftime('%H:%M')} - "
                f"{(self.end_at + timedelta(hours=3)).strftime('%H:%M')}"
            )

        return f"{self.start_at_as_str} - {self.end_at_as_str}"

    @property
    def all_purchased(self):
        data = self.event.purchase_events.filter(
            start_at=self.start_at, end_at=self.end_at, purchase__status__in=["SUCCESS", "VISITED"]
        )
        return data.aggregate(models.Sum("count"))["count__sum"] if data else 0

    @property
    def lefts_visitors_sum(self):
        return self.event.max_visitors - self.all_purchased

    @property
    def lefts_visitors_by_cat(self):
        max_lefts_visitors = self.lefts_visitors_sum

        total_purchased = 0

        result = {}
        for cat in EventPriceCategory.values:
            started = self.prices.filter(category=cat).first()
            if not started:
                result[cat] = 0
                continue

            purchased = self.event.purchase_events.filter(
                category=cat, start_at=self.start_at, end_at=self.end_at, purchase__status__in=["SUCCESS", "VISITED"]
            )
            if not purchased:
                result[cat] = started.max_visitors
                continue
            purchased_val = purchased.aggregate(models.Sum("count"))["count__sum"]

            category_lefts_visitors = started.max_visitors - purchased_val
            total_purchased += purchased_val

            if category_lefts_visitors > max_lefts_visitors:
                result[cat] = max_lefts_visitors
                continue

            result[cat] = category_lefts_visitors

        if total_purchased >= self.event.max_visitors:
            for cat in EventPriceCategory.values:
                result[cat] = 0

        return result

    @property
    def prices_info(self):
        result = {}
        for cat in EventPriceCategory.values:
            event_price = self.prices.filter(category=cat).first()
            if not event_price:
                result[f"max_visitors_{cat.lower()}"] = "-"
                result[f"purchase_{cat.lower()}"] = "-"
                result[f"price_{cat.lower()}"] = "-"
                continue

            result[f"price_{cat.lower()}"] = event_price.price
            result[f"max_visitors_{cat.lower()}"] = event_price.max_visitors

            purchases = self.event.purchase_events.filter(
                category=cat, start_at=self.start_at, end_at=self.end_at, purchase__status="SUCCESS"
            )
            result[f"purchase_{cat.lower()}"] = (
                f"{purchases.aggregate(models.Sum("count"))["count__sum"] if purchases else 0}"
                f"/"
                f"{event_price.max_visitors}"
            )

        return result

    def __str__(self):
        return f"{self.event.name} старт в {self.start_at}"

    def get_absolute_url(self):
        return reverse("events:event-detail", args=[self.event_id])

    class Meta:
        verbose_name = "Расписание мероприятия"
        verbose_name_plural = "Расписания мероприятий"
        ordering = ["start_at"]


class EventPriceCategory(models.TextChoices):
    STANDARD = "STANDARD"
    CHILD = "CHILD"
    STUDENT = "STUDENT"
    RETIREE = "RETIREE"


class EventSchedulePrice(models.Model):
    event_schedule = models.ForeignKey(EventSchedule, models.CASCADE, "prices", verbose_name="Время мероприятия")
    price = models.PositiveIntegerField("Цена")
    category = models.CharField("Категория покупателя", max_length=255, choices=EventPriceCategory.choices)
    max_visitors = models.PositiveIntegerField("Максимальное количество посетителей категории")
    bitrix_id = models.PositiveIntegerField("ID в Bitrix", blank=True, null=True)

    def __str__(self):
        return f'{self.event_schedule} для категории  "{self.category}"'

    class Meta:
        verbose_name = "Вариант билета"
        verbose_name_plural = "Варианты билета"
        ordering = ["event_schedule_id", "category"]


class EventSet(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    events = models.ManyToManyField(Event, "sets", verbose_name="Мероприятия")
    price = models.PositiveIntegerField("Цена")
    set_id = models.UUIDField("ID единого билета", default=uuid.uuid4(), editable=False)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("events:event_set-detail", args=[self.id])

    class Meta:
        verbose_name = "Набор мероприятий"
        verbose_name_plural = "Наборы мероприятий"
        ordering = ["id"]
