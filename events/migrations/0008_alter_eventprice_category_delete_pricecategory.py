# Generated by Django 5.0.6 on 2024-06-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0007_organization_description"),
        ("tickets", "0004_alter_purchaseevent_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventprice",
            name="category",
            field=models.CharField(
                choices=[
                    ("Стандартный", "Standard"),
                    ("Детский", "Child"),
                    ("Студенческий", "Student"),
                    ("Пенсионер", "Retiree"),
                ],
                max_length=255,
                verbose_name="Категория покупателя",
            ),
        ),
        migrations.DeleteModel(
            name="PriceCategory",
        ),
    ]