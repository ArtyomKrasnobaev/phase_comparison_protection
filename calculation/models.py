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


class SettingsCalculationProtocol(models.Model):
    """Модель протокола расчета параметра настройки органа."""

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

    def __str__(self):

        meta = f'{self.component} {self.protection_half_set}'
        return meta


class FaultCalculationProtocol(models.Model):
    """Модель протокола расчета токов КЗ."""

    protection_half_set = models.ForeignKey(
        ProtectionHalfSet, on_delete=models.CASCADE, related_name="faults"
    )
    fault_type = models.CharField(verbose_name="Вид КЗ", max_length=255)
    fault_location = models.CharField(verbose_name="Узел КЗ", max_length=255)
    network_topology = models.CharField(verbose_name="Схема сети", max_length=255)
    positive_sequence_current = models.FloatField(
        verbose_name="Ток прямой последовательности"
    )
    negative_sequence_current = models.FloatField(
        verbose_name="Ток обратной последовательности"
    )

    class Meta:
        """Мета-данные модели FaultCalculation."""

        verbose_name = "Протокол расчета КЗ"
        verbose_name_plural = "Протоколы расчетов КЗ"


class SensitivityAnalysisProtocol(models.Model):
    """Модель анализа чувствительности."""

    settings_calculation_protocol = models.ForeignKey(
        SettingsCalculationProtocol, on_delete=models.CASCADE
    )
    fault_calculation_protocol = models.ForeignKey(
        FaultCalculationProtocol, on_delete=models.CASCADE
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
