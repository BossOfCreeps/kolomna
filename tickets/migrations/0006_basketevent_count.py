# Generated by Django 5.0.6 on 2024-06-11 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0005_alter_purchaseevent_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="basketevent",
            name="count",
            field=models.PositiveIntegerField(default=0, verbose_name="Количество"),
        ),
    ]
