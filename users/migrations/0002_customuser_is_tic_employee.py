# Generated by Django 5.0.6 on 2024-06-13 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_tic_employee",
            field=models.BooleanField(default=False),
        ),
    ]
