from django.core.management import BaseCommand

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
        Substation.objects.all().delete()
        Component.objects.all().delete()
        ProtectionDevice.objects.all().delete()
        ProtectionHalfSet.objects.all().delete()

        # Заполнение таблицы ЛЭП
        line = Line.objects.create(dispatch_name="ВЛ 500 кВ Ново-Анжерская - Томская")

        # Заполнение таблицы подстанций
        substations = Substation.objects.bulk_create(
            [
                Substation(dispatch_name="ПС 500 кВ Ново-Анжерская"),
                Substation(dispatch_name="ПС 500 кВ Томская"),
            ]
        )

        # Заполнение таблицы органов ДФЗ
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

        # Заполнение таблицы устройств РЗА
        protection_device = ProtectionDevice.objects.create(
            device_model="ШЭ2710 582", manufacturer="НПП ЭКРА"
        )
        protection_device.components.set(components)

        # Заполнение таблицы полукомплектов ДФЗ
        ProtectionHalfSet.objects.bulk_create(
            [
                ProtectionHalfSet(
                    line=line,
                    substation=substations[0],
                    protection_device=protection_device,
                ),
                ProtectionHalfSet(
                    line=line,
                    substation=substations[1],
                    protection_device=protection_device,
                ),
            ]
        )

        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена"))
