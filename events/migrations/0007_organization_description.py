# Generated by Django 5.0.6 on 2024-06-11 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_alter_eventschedule_end_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="organization",
            name="description",
            field=models.TextField(default="", verbose_name="Описание"),
            preserve_default=False,
        ),
    ]
