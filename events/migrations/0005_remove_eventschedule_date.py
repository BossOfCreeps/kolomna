# Generated by Django 5.0.6 on 2024-06-11 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_organization_file"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventschedule",
            name="date",
        ),
    ]
