# Generated by Django 5.0.6 on 2024-06-14 13:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0026_alter_eventset_set_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={
                "ordering": ["id"],
                "verbose_name": "Мероприятие",
                "verbose_name_plural": "Мероприятия",
            },
        ),
        migrations.AlterModelOptions(
            name="eventimage",
            options={"ordering": ["id"]},
        ),
        migrations.AlterModelOptions(
            name="eventschedule",
            options={
                "ordering": ["start_at"],
                "verbose_name": "Расписание мероприятия",
                "verbose_name_plural": "Расписания мероприятий",
            },
        ),
        migrations.AlterModelOptions(
            name="eventscheduleprice",
            options={
                "ordering": ["event_schedule_id", "category"],
                "verbose_name": "Вариант билета",
                "verbose_name_plural": "Варианты билета",
            },
        ),
        migrations.AlterModelOptions(
            name="eventset",
            options={
                "ordering": ["id"],
                "verbose_name": "Набор мероприятий",
                "verbose_name_plural": "Наборы мероприятий",
            },
        ),
        migrations.AlterModelOptions(
            name="organization",
            options={
                "ordering": ["id"],
                "verbose_name": "Организация",
                "verbose_name_plural": "Организации",
            },
        ),
        migrations.AlterField(
            model_name="eventset",
            name="set_id",
            field=models.UUIDField(
                default=uuid.UUID("9eebc448-0914-4e45-bdff-b185e4843f2e"),
                editable=False,
                verbose_name="ID единого билета",
            ),
        ),
    ]