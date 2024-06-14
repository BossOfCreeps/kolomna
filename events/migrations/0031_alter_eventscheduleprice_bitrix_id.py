# Generated by Django 5.0.6 on 2024-06-14 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0030_eventset_bitrix_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventscheduleprice",
            name="bitrix_id",
            field=models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name="ID в Bitrix"),
        ),
    ]
