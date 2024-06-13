# Generated by Django 5.0.6 on 2024-06-13 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0018_alter_eventschedule_group_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="abbreviation",
            field=models.CharField(
                default="", max_length=1024, verbose_name="Аббревиатура"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="organization",
            name="abbreviation",
            field=models.CharField(
                default="", max_length=1024, verbose_name="Аббревиатура"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="organization",
            name="color",
            field=models.CharField(default="", max_length=64, verbose_name="Цвет"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="organization",
            name="short_name",
            field=models.CharField(
                default="", max_length=1024, verbose_name="Короткое название"
            ),
            preserve_default=False,
        ),
    ]
