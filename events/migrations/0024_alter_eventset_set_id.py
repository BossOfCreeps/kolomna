# Generated by Django 5.0.6 on 2024-06-14 06:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0023_eventset_set_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventset",
            name="set_id",
            field=models.UUIDField(
                default=uuid.UUID("8082e36b-7328-4ba6-b05a-75826ed6ffca"),
                verbose_name="ID единого билета",
            ),
        ),
    ]