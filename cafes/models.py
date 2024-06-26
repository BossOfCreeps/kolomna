from random import randint

from django.db import models


class Cafe(models.Model):
    name = models.CharField("Название", max_length=1024)
    file = models.ImageField(upload_to="media/cafes", null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def rate():
        return randint(1, 5)

    class Meta:
        verbose_name = "Кафе"
        verbose_name_plural = "Кафе"
