from django.db import models

from events.models import EventPrice, EventSchedule
from users.models import CustomUser


class BasketEvent(models.Model):
    event_price = models.ForeignKey(EventPrice, models.CASCADE, "basket_events", verbose_name="Цена")
    event_schedule = models.ForeignKey(EventSchedule, models.CASCADE, "basket_events", verbose_name="Расписание")
    user = models.ForeignKey(CustomUser, models.CASCADE, "basket_events", verbose_name="Пользователь")

    def __str__(self):
        return f"{self.event_price} | {self.event_schedule} | {self.user}"

    class Meta:
        verbose_name = "Мероприятие в корзине"
        verbose_name_plural = "Мероприятия в корзине"
