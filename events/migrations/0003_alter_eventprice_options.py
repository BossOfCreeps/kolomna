# Generated by Django 5.0.6 on 2024-06-11 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_eventprice_bitrix_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eventprice",
            options={
                "verbose_name": "Вариант билета",
                "verbose_name_plural": "Варианты билета",
            },
        ),
    ]