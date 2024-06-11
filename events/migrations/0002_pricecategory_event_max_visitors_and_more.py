# Generated by Django 5.0.6 on 2024-06-11 01:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
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
        migrations.AddField(
            model_name="event",
            name="max_visitors",
            field=models.PositiveIntegerField(
                default=1, verbose_name="Максимальное количество посетителей всего"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="events.organization",
                verbose_name="Организация",
            ),
        ),
        migrations.AlterField(
            model_name="eventimage",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="events.event",
                verbose_name="Мероприятие",
            ),
        ),
        migrations.AlterField(
            model_name="eventschedule",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schedules",
                to="events.event",
                verbose_name="Мероприятие",
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
                    models.PositiveIntegerField(
                        verbose_name="Максимальное количество посетителей категории"
                    ),
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
