# Generated by Django 5.0.6 on 2024-06-15 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0019_purchase_bitrix_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewimage",
            name="rate",
            field=models.PositiveIntegerField(default=5, verbose_name="Рейтинг"),
            preserve_default=False,
        ),
    ]