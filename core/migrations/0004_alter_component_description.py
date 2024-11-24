# Generated by Django 4.2.16 on 2024-11-24 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="component",
            name="description",
            field=models.TextField(
                blank=True,
                null=True,
                unique=True,
                verbose_name="Описание работы органа",
            ),
        ),
    ]
