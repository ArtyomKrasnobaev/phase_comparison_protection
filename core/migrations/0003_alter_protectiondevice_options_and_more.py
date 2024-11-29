# Generated by Django 4.2.16 on 2024-11-29 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_line_pf_name_substation_pf_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="protectiondevice",
            options={
                "verbose_name": "Устройство РЗА",
                "verbose_name_plural": "Устройства РЗА",
            },
        ),
        migrations.RemoveField(
            model_name="protectiondevice",
            name="components",
        ),
        migrations.AddField(
            model_name="line",
            name="length",
            field=models.FloatField(
                blank=True, null=True, verbose_name="Длина ЛЭП, км"
            ),
        ),
        migrations.AlterField(
            model_name="line",
            name="current_capacity",
            field=models.FloatField(default=2000, verbose_name="ДДТН, А"),
        ),
        migrations.CreateModel(
            name="DeviceEquipment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "component",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_equipment",
                        to="core.component",
                    ),
                ),
                (
                    "protection_device",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_equipment",
                        to="core.protectiondevice",
                    ),
                ),
            ],
            options={
                "verbose_name": "Орган ДФЗ устройства РЗА",
                "verbose_name_plural": "Органы ДФЗ устройства РЗА",
            },
        ),
    ]
