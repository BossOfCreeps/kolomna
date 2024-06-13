import uuid

from django.db import models

from helpers import add_product, datetime_to_str, date_to_str


class Organization(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    file = models.ImageField(upload_to="media/organizations", null=True, blank=True)
    address = models.TextField("Адрес")
    latitude = models.FloatField("Широта")
    longitude = models.FloatField("Долгота")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Event(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE, "events", verbose_name="Организация")

    name = models.CharField("Название", max_length=1024)
    age_limit = models.CharField("Возрастной ценз", max_length=1024)
    html_description = models.TextField("HTML описание")
    duration = models.PositiveIntegerField("Длительность в минутах")
    max_visitors = models.PositiveIntegerField("Максимальное количество посетителей всего")

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class EventImage(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, "images", verbose_name="Мероприятие")
    file = models.ImageField(upload_to="media/events")


class EventSchedule(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, "schedules", verbose_name="Мероприятие")
    group_id = models.UUIDField("Группа", default=uuid.uuid4)
    start_at = models.DateTimeField("Дата и время начало")
    end_at = models.DateTimeField("Дата и время конца")

    @property
    def start_at_as_str(self):
        return datetime_to_str(self.start_at)

    @property
    def end_at_as_str(self):
        return datetime_to_str(self.end_at)

    @property
    def date_range(self):
        if self.start_at.date() == self.end_at.date():
            return (
                f"{date_to_str(self.start_at.date())} "
                f"{self.start_at.strftime('%H:%M')} - {self.end_at.strftime('%H:%M')}"
            )

        return f"{self.start_at_as_str} - {self.end_at_as_str}"

    @property
    def lefts_visitors(self):
        max_lefts_visitors = self.event.max_visitors
        all_purchased = self.event.purchase_events.filter(start_at=self.start_at, end_at=self.end_at)
        if all_purchased:
            max_lefts_visitors -= all_purchased.aggregate(models.Sum("count"))["count__sum"]

        result = {}
        for cat in EventPriceCategory.values:
            started = self.prices.filter(category=cat).first()
            if not started:
                result[cat] = 0
                continue

            purchased = self.event.purchase_events.filter(category=cat, start_at=self.start_at, end_at=self.end_at)
            if not purchased:
                result[cat] = started.max_visitors
                continue

            category_lefts_visitors = started.max_visitors - purchased.aggregate(models.Sum("count"))["count__sum"]
            if category_lefts_visitors > max_lefts_visitors:
                result[cat] = max_lefts_visitors
                continue

            result[cat] = category_lefts_visitors

        return result

    def __str__(self):
        return f"{self.event.name} старт в {self.start_at}"

    class Meta:
        verbose_name = "Расписание мероприятия"
        verbose_name_plural = "Расписания мероприятий"


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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if self.bitrix_id is None:
            self.bitrix_id = add_product(
                f'"{self.event_schedule.event.name}" для категории "{self.category}"', self.price
            )
            super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.event_schedule} для категории  "{self.category}"'

    class Meta:
        verbose_name = "Вариант билета"
        verbose_name_plural = "Варианты билета"
