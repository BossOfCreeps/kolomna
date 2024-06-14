# Generated by Django 5.0.6 on 2024-06-14 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0016_purchaseevent_set_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="purchaseevent",
            name="set_id",
        ),
        migrations.AddField(
            model_name="purchase",
            name="set_id",
            field=models.UUIDField(blank=True, null=True, verbose_name="ID единого билета"),
        ),
    ]
