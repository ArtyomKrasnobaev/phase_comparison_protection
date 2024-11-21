from django.core.management import BaseCommand

from calculation.models import *
from core.models import *


class Command(BaseCommand):
    """
    Команда для автоматического заполнения БД тестовыми данными.

    Запуск:
        python manage.py seed_db
    """

    def handle(self, *args, **options):
        """Метод заполнения БД тестовыми данными."""

        Line.objects.all().delete()
        ProtectionDevice.objects.all().delete()
        Component.objects.all().delete()
        CalculationProtocol.objects.all().delete()

        components = Component.objects.bulk_create(
            [
                Component(setting_designation="IЛ БЛОК"),
                Component(setting_designation="IЛ ОТКЛ"),
                Component(setting_designation="I2 БЛОК"),
                Component(setting_designation="I2 ОТКЛ"),
                Component(setting_designation="DI2 БЛОК"),
                Component(setting_designation="DI2 ОТКЛ"),
                Component(setting_designation="U2 БЛОК"),
                Component(setting_designation="U2 ОТКЛ"),
            ]
        )

        protection_device = ProtectionDevice.objects.create(
            device_model="ШЭ2710 582", manufacturer="НПП ЭКРА"
        )
        protection_device.components.set(components)

        Line.objects.bulk_create(
            [
                Line(
                    dispatch_name="ВЛ 500 кВ Ново-Анжерская - Томская",
                    current_capacity=2000,
                    protection_device=protection_device,
                ),
                Line(
                    dispatch_name="ВЛ 500 кВ Итатская - Томская",
                    current_capacity=2000,
                    protection_device=protection_device,
                ),
                Line(
                    dispatch_name="ВЛ 500 кВ Заря - Юрга",
                    current_capacity=2000,
                    protection_device=protection_device,
                ),
            ]
        )

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена"))
