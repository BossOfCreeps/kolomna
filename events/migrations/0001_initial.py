# Generated by Django 5.0.6 on 2024-06-11 03:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1024, verbose_name="Название")),
                ("html_description", models.TextField(verbose_name="HTML описание")),
                (
                    "duration",
                    models.PositiveIntegerField(verbose_name="Длительность в минутах"),
                ),
                (
                    "max_visitors",
                    models.PositiveIntegerField(verbose_name="Максимальное количество посетителей всего"),
                ),
            ],
            options={
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
            },
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=1024, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Организация",
                "verbose_name_plural": "Организации",
            },
        ),
        migrations.CreateModel(
            name="PriceCategory",
            fields=[
                (
                    "code",
                    models.CharField(
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Код категории",
                    ),
                ),
                ("name", models.CharField(max_length=1024, verbose_name="Название")),
            ],
            options={
                "verbose_name": "Категория покупателя",
                "verbose_name_plural": "Категория покупателя",
            },
        ),
        migrations.CreateModel(
            name="EventImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.ImageField(upload_to="media/events")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="events.event",
                        verbose_name="Мероприятие",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(blank=True, null=True, verbose_name="Дата мероприятия"),
                ),
                (
                    "start_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="Дата и время начало"),
                ),
                (
                    "end_at",
                    models.DateTimeField(blank=True, null=True, verbose_name="Дата и время конца"),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="events.event",
                        verbose_name="Мероприятие",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="events.organization",
                verbose_name="Организация",
            ),
        ),
        migrations.CreateModel(
            name="EventPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.PositiveIntegerField(verbose_name="Цена")),
                (
                    "max_visitors",
                    models.PositiveIntegerField(verbose_name="Максимальное количество посетителей категории"),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices",
                        to="events.event",
                        verbose_name="Мероприятие",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="events.pricecategory",
                        verbose_name="Категория покупателя",
                    ),
                ),
            ],
        ),
    ]
