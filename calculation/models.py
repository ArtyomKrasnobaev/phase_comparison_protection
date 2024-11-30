from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.models import Component, Line, ProtectionHalfSet


class CalculationMeta(models.Model):
    """Модель мета-данных расчета."""

    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='calculations', null=True, blank=True)
    calculation_number = models.PositiveIntegerField(
        verbose_name="Номер расчета", null=True, blank=True
    )
    calculation_date = models.DateTimeField(verbose_name="Дата расчета", auto_now_add=True)

    class Meta:
        """Мета-данные модели CalculationMeta."""

        verbose_name = "Мета-данные расчета"
        verbose_name_plural = "Мета-данные расчетов"

    def __str__(self):
        """
        :return: Номер расчета.
        """

        return f'Расчет параметров настройки ДФЗ {self.line} от {self.calculation_date}'


class SettingsCalculation(models.Model):
    """Модель протокола расчета параметра настройки органа."""

    calculation_meta = models.ForeignKey(
        CalculationMeta, on_delete=models.CASCADE, related_name='settings_calculations'
    )
    protection_half_set = models.ForeignKey(
        ProtectionHalfSet, on_delete=models.CASCADE, related_name='settings_calculations'
    )
    component = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name='settings_calculations'
    )
    result_value = models.FloatField(verbose_name="Результат расчета")

    class Meta:
        """Мета-данные модели CalculationData."""

        verbose_name = "Протокол расчета"
        verbose_name_plural = "Протоколы расчетов"


class FaultCalculation(models.Model):
    """Модель протокола расчета токов КЗ."""

    protection_half_set = models.ForeignKey(
        ProtectionHalfSet, on_delete=models.CASCADE, related_name="fault_calculations"
    )
    fault_type = models.CharField(verbose_name="Вид КЗ", max_length=255)
    fault_location = models.CharField(verbose_name="Узел КЗ", max_length=255)
    network_topology = models.CharField(verbose_name="Схема сети", max_length=255)
    fault_values = models.JSONField()

    class Meta:
        """Мета-данные модели FaultCalculation."""

        verbose_name = "Расчет токов КЗ"
        verbose_name_plural = "Протоколы расчетов токов КЗ"


class SensitivityAnalysis(models.Model):
    """Модель анализа чувствительности."""

    settings_calculation = models.ForeignKey(
        SettingsCalculation, on_delete=models.CASCADE, related_name='sensitivity_analysis'
    )
    fault_calculation = models.ForeignKey(
        FaultCalculation, on_delete=models.CASCADE, related_name='sensitivity_analysis'
    )
    sensitivity_rate = models.FloatField(verbose_name="Коэффициент чувствительности")

    class Meta:
        """Мета-данные модели SensitivityAnalysis."""

        verbose_name = "Анализ чувствительности"
        verbose_name_plural = "Анализ чувствительности"


@receiver(pre_save, sender=CalculationMeta)
def generate_calculation_number(sender, instance, **kwargs):
    """Генерация номера расчета перед сохранением."""

    if not instance.calculation_number:
        last_calculation = (
            CalculationMeta.objects.all().order_by("calculation_number").last()
        )
        if last_calculation:
            instance.calculation_number = last_calculation.calculation_number + 1
        else:
            instance.calculation_number = 1
