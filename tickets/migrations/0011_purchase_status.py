# Generated by Django 5.0.6 on 2024-06-13 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0010_remove_basketevent_event_schedule_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="status",
            field=models.CharField(
                choices=[("NEW", "New"), ("SUCCESS", "Success"), ("CLOSED", "Closed")],
                default="NEW",
                max_length=255,
                verbose_name="Статус",
            ),
        ),
    ]
