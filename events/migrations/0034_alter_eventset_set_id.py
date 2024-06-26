# Generated by Django 5.0.6 on 2024-06-16 00:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0033_remove_eventset_bitrix_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventset",
            name="set_id",
            field=models.UUIDField(
                default=uuid.UUID("348daa1a-1af9-4946-a50d-0dbc3a7c1353"),
                editable=False,
                verbose_name="ID единого билета",
            ),
        ),
    ]
