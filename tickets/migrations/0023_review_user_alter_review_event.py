# Generated by Django 5.0.6 on 2024-06-15 02:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0033_remove_eventset_bitrix_id"),
        ("tickets", "0022_remove_review_purchase_review_event"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="review",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews",
                to="events.event",
                verbose_name="Мероприятие",
            ),
        ),
    ]