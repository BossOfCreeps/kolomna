from django.conf import settings
from django.db import models
from django.urls import reverse

from events.models import EventSchedulePrice, EventSchedule, Event, EventPriceCategory, Organization, EventSet
from helpers import date_to_str, datetime_to_str, send_email
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
    VISITED = "VISITED"
    CLOSED = "CLOSED"


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, models.CASCADE, "purchases", verbose_name="Пользователь")
    created_at = models.DateTimeField("Дата и время покупки", auto_now_add=True)
    qr_code = models.ImageField(upload_to="media/purchases/qr_code", verbose_name="QR-код", null=True, blank=True)
    status = models.CharField("Статус", max_length=255, choices=PurchaseStatus.choices, default=PurchaseStatus.NEW)
    yookassa_url = models.URLField("Ссылка", null=True, blank=True)
    total_price = models.PositiveIntegerField("Стоимость")
    set_id = models.UUIDField("ID единого билета", blank=True, null=True)
    bitrix_id = models.PositiveIntegerField("ID в Bitrix", blank=True, null=True)

    @property
    def title(self):
        if self.set_id:
            return f'#{self.id} Набор "{EventSet.objects.get(set_id=self.set_id).name}"'
        else:
            return f'#{self.id} Билет "{self.events.first().event.name}"'

    @property
    def organizations(self):
        return Organization.objects.filter(pk__in=self.events.values_list("event__organization", flat=True))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        if self.status == PurchaseStatus.SUCCESS.value:
            message = f"""<img src="{settings.SERVER_URL}{self.qr_code.url}" width="200" height="200"><table>"""

            for event in self.events.all():
                message += f"""
                <tr>
                    <td style="border: 1px solid black;">{event.date_range}</td>
                    <td style="border: 1px solid black;">{event.event.name}</td>
                    <td style="border: 1px solid black;">{event.event.organization.address}</td>
                </tr>
                """

            message += "</table><br>"

            send_email(self.title, message, [self.user.email])

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

    def __str__(self):
        return f"{self.event} | {self.start_at} | {self.category}"

    class Meta:
        verbose_name = "Купленное мероприятие"
        verbose_name_plural = "Купленное мероприятие"
        ordering = ["start_at"]


class Review(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, "reviews", verbose_name="Мероприятие")
    user = models.ForeignKey(CustomUser, models.CASCADE, "reviews", verbose_name="Пользователь")
    text = models.TextField("Текст")
    rate = models.PositiveIntegerField("Рейтинг")
    created_at = models.DateTimeField("Дата", auto_now_add=True)

    @staticmethod
    def get_absolute_url():
        return reverse("users:profile")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, models.CASCADE, "images", verbose_name="Отзыв")
    file = models.ImageField(upload_to="media/reviews", verbose_name="Изображение")
