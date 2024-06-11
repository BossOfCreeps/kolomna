from django.db import models

from helpers import add_product


class Organization(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    file = models.ImageField(upload_to="media/organizations", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"


class Event(models.Model):
    organization = models.ForeignKey(Organization, models.CASCADE, "events", verbose_name="Организация")

    name = models.CharField("Название", max_length=1024)
    html_description = models.TextField("HTML описание")
    duration = models.PositiveIntegerField("Длительность в минутах")
    max_visitors = models.PositiveIntegerField("Максимальное количество посетителей всего")

    @property
    def duration_as_str(self):
        return f"{round(self.duration/60, 1)} часа"

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
    start_at = models.DateTimeField("Дата и время начало")
    end_at = models.DateTimeField("Дата и время конца")

    def __str__(self):
        return f"{self.event.name} старт в {self.start_at}"


class PriceCategory(models.Model):
    code = models.CharField("Код категории", max_length=32, primary_key=True)
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория покупателя"
        verbose_name_plural = "Категория покупателя"


class EventPrice(models.Model):
    event = models.ForeignKey(Event, models.CASCADE, "prices", verbose_name="Мероприятие")
    price = models.PositiveIntegerField("Цена")
    category = models.ForeignKey(PriceCategory, models.CASCADE, verbose_name="Категория покупателя")
    max_visitors = models.PositiveIntegerField("Максимальное количество посетителей категории")
    bitrix_id = models.PositiveIntegerField("ID в Bitrix", blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        self.bitrix_id = add_product(f'"{self.event.name}" для категории "{self.category.name}"', self.price)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.event.name} для категории  "{self.category.name}"'

    class Meta:
        verbose_name = "Вариант билета"
        verbose_name_plural = "Варианты билета"
