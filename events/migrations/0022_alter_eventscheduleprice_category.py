# Generated by Django 5.0.6 on 2024-06-14 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0021_alter_eventscheduleprice_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventscheduleprice",
            name="category",
            field=models.CharField(
                choices=[
                    ("STANDARD", "Standard"),
                    ("CHILD", "Child"),
                    ("STUDENT", "Student"),
                    ("RETIREE", "Retiree"),
                ],
                max_length=255,
                verbose_name="Категория покупателя",
            ),
        ),
    ]