from django.db import models

from events.models import EventSchedulePrice, EventSchedule, Event, EventPriceCategory, Organization, EventSet
from users.models import CustomUser


class BasketEvent(models.Model):
    event_price = models.ForeignKey(EventSchedulePrice, models.CASCADE, "basket_events", verbose_name="Цена")
    user = models.ForeignKey(CustomUser, models.CASCADE, "basket_events", verbose_name="Пользователь")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество")
    set_id = models.UUIDField("ID единого билета", blank=True, null=True)

    def __str__(self):
        return f"{self.event_price} | {self.user}"

    class Meta:
        verbose_name = "Мероприятие в корзине"
        verbose_name_plural = "Мероприятия в корзине"


class PurchaseStatus(models.TextChoices):
    NEW = "NEW"
    SUCCESS = "SUCCESS"
    CLOSED = "CLOSED"


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, "purchases", verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата и время покупки", auto_now_add=True)
    qr_code = models.ImageField(upload_to="media/purchases/qr_code", verbose_name="QR-код", null=True, blank=True)
    status = models.CharField("Статус", max_length=255, choices=PurchaseStatus.choices, default=PurchaseStatus.NEW)
    yookassa_url = models.URLField("Ссылка", null=True, blank=True)
    total_price = models.PositiveIntegerField("Стоимость")
    set_id = models.UUIDField("ID единого билета", blank=True, null=True)

    @property
    def title(self):
        if self.set_id:
            return f'Единый билет "{EventSet.objects.get(set_id=self.set_id).name}"'
        else:
            return f'Билет "{self.events.first().event.name}"'

    @property
    def organizations(self):
        return Organization.objects.filter(pk__in=self.events.values_list("event__organization", flat=True))

    def __str__(self):
        return f"{self.user} | {self.created_at.isoformat()}"

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"


class PurchaseEvent(models.Model):
    purchase = models.ForeignKey(Purchase, models.CASCADE, "events", verbose_name="Покупка")
    event = models.ForeignKey(Event, models.CASCADE, "purchase_events", verbose_name="Мероприятие")
    count = models.PositiveIntegerField("Количество")

    category = models.CharField("Категория покупателя", max_length=255, choices=EventPriceCategory.choices)
    price = models.PositiveIntegerField("Цена")

    start_at = models.DateTimeField("Дата и время начало")
    end_at = models.DateTimeField("Дата и время конца")

    def __str__(self):
        return f"{self.event} | {self.start_at} | {self.category}"

    class Meta:
        verbose_name = "Купленное мероприятие"
        verbose_name_plural = "Купленное мероприятие"
        ordering = ["start_at"]
