# Generated by Django 5.0.6 on 2024-06-12 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0013_remove_eventprice_event_eventscheduleprice"),
        ("tickets", "0010_remove_basketevent_event_schedule_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="EventPrice",
        ),
    ]