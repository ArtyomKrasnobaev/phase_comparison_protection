from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Component, ProtectionHalfSet


class CalculationMeta(models.Model):
    """Модель мета-данных расчета."""

    calculation_number = models.PositiveIntegerField(
        verbose_name="Номер расчета", null=True, blank=True
    )
    timestamp = models.DateTimeField(verbose_name="Дата расчета", auto_now_add=True)

    class Meta:
        """Мета-данные модели CalculationMeta."""

        verbose_name = "Мета-данные расчета"
        verbose_name_plural = "Мета-данные расчетов"

    def __str__(self):
        """
        :return: Номер расчета.
        """

        return str(self.calculation_number)


class CalculationProtocol(models.Model):
    """Модель протокола расчета."""

    calculation_meta = models.ForeignKey(
        CalculationMeta, on_delete=models.CASCADE, related_name="protocols"
    )
    protection_half_set = models.ForeignKey(
        ProtectionHalfSet, on_delete=models.CASCADE, related_name="protocols"
    )
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="protocols"
    )
    result_value = models.FloatField(verbose_name="Результат расчета")

    class Meta:
        """Мета-данные модели CalculationData."""

        verbose_name = "Протокол расчета"
        verbose_name_plural = "Протоколы расчетов"


class FaultCalculation(models.Model):
    """Модель данных расчета токов КЗ."""

    calculation_meta = models.ForeignKey(
        CalculationMeta, on_delete=models.CASCADE, related_name="faults"
    )
    protection_half_set = models.ForeignKey(
        ProtectionHalfSet, on_delete=models.CASCADE, related_name="faults"
    )
    fault_type = models.CharField(verbose_name="Вид КЗ", max_length=255)
    fault_location = models.CharField(verbose_name="Узел КЗ", max_length=255)
    network_topology = models.CharField(verbose_name="Схема сети", max_length=255)
    fault_currents = models.JSONField(verbose_name="Токи симметричных составляющих")

    class Meta:
        """Мета-данные модели FaultCalculation."""

        verbose_name = "Протокол расчета КЗ"
        verbose_name_plural = "Протоколы расчетов КЗ"


@receiver(pre_save, sender=CalculationMeta)
def generate_calculation_number(sender, instance, **kwargs):
    """Автогенерация номера расчета перед сохранением."""
    if not instance.calculation_number:  # Если номер расчета еще не задан
        # Получаем максимальный номер расчета и увеличиваем на 1
        last_calculation = (
            CalculationMeta.objects.all().order_by("calculation_number").last()
        )
        if last_calculation:
            instance.calculation_number = last_calculation.calculation_number + 1
        else:
            instance.calculation_number = 1  # Если записей нет, начинаем с 1
