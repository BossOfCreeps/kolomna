# Generated by Django 5.0.6 on 2024-06-12 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0014_delete_eventprice"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventschedule",
            options={
                "verbose_name": "Расписание мероприятия",
                "verbose_name_plural": "Расписания мероприятий",
            },
        ),
    ]
