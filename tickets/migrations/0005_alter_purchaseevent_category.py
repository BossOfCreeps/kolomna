# Generated by Django 5.0.6 on 2024-06-11 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0004_alter_purchaseevent_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchaseevent",
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
