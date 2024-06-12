from django.db import models

from events.models import EventPrice, EventSchedule, Event, EventPriceCategory
from users.models import CustomUser


class BasketEvent(models.Model):
    event_price = models.ForeignKey(EventPrice, models.CASCADE, "basket_events", verbose_name="Цена")
    event_schedule = models.ForeignKey(EventSchedule, models.CASCADE, "basket_events", verbose_name="Расписание")
    user = models.ForeignKey(CustomUser, models.CASCADE, "basket_events", verbose_name="Пользователь")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество")

    def __str__(self):
        return f"{self.event_price} | {self.event_schedule} | {self.user}"

    class Meta:
        verbose_name = "Мероприятие в корзине"
        verbose_name_plural = "Мероприятия в корзине"


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, "purchases", verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата и время покупки", auto_now_add=True)

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
        return f"{self.event} | {self.purchase} | {self.category}"

    class Meta:
        verbose_name = "Купленное мероприятие"
        verbose_name_plural = "Купленное мероприятие"
        ordering = ["start_at"]
