# Generated by Django 5.0.6 on 2024-06-14 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0028_alter_eventset_set_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventset",
            name="set_id",
            field=models.UUIDField(default="0", editable=False, verbose_name="ID единого билета"),
        ),
    ]
