# Generated by Django 5.0.6 on 2024-06-14 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0018_review_reviewimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="purchase",
            name="bitrix_id",
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name="ID в Bitrix"),
        ),
    ]
