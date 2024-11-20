from django.db import models


class Component(models.Model):
    """Модель органа защиты для реализации функции ДФЗ."""

    setting_designation = models.CharField(
        verbose_name="Обозначение параметра настройки", max_length=100, unique=True
    )

    class Meta:
        """Мета-данные модели Component."""

        verbose_name = "Орган ДФЗ"
        verbose_name_plural = "Органы ДФЗ"

    def __str__(self):
        """Возвращает обозначение параметра настройки органа."""

        return self.setting_designation


class ProtectionDevice(models.Model):
    """Модель устройства защиты с функцией ДФЗ."""

    device_model = models.CharField(
        verbose_name="Модель устройства", max_length=100, unique=True
    )
    manufacturer = models.CharField(verbose_name="Производитель", max_length=100)
    components = models.ManyToManyField(Component, related_name="protection_device")

    class Meta:
        """Мета-данные модели ProtectionDevice."""

        verbose_name = "Устройство защиты"
        verbose_name_plural = "Устройства защиты"

    def __str__(self):
        """Возвращает модель устройства защиты."""

        return self.device_model


class Line(models.Model):
    """
    Модель линии электропередач (ЛЭП).

    ЛЭП напряжением 110 кВ и выше с двусторонним питанием без ответвлений.
    """

    dispatch_name = models.CharField(
        verbose_name="Диспетчерское наименование", max_length=100, unique=True
    )
    current_capacity = models.FloatField(verbose_name="ДДТН", default=2000)
    protection_device = models.ForeignKey(ProtectionDevice, on_delete=models.CASCADE)

    class Meta:
        """Мета-данные модели Line."""

        verbose_name = "ЛЭП"
        verbose_name_plural = "ЛЭП"

    def __str__(self):
        """Возвращает диспетчерское наименование ЛЭП."""

        return self.dispatch_name
