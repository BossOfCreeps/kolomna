# Generated by Django 5.0.6 on 2024-06-12 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0010_organization_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventprice",
            name="left_visitors",
            field=models.PositiveIntegerField(default=0, verbose_name="Осталось мест"),
            preserve_default=False,
        ),
    ]
