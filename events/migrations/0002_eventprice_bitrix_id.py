# Generated by Django 5.0.6 on 2024-06-11 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventprice",
            name="bitrix_id",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="ID в Bitrix"
            ),
        ),
    ]
