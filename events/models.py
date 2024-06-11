from django.db import models


class Organization(models.Model):
    name = models.CharField("Название", max_length=1024)

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
    data = models.JSONField()  # TODO: Описать в README


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
