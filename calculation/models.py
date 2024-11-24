from django.db import models

from core.models import Component, ProtectionHalfSet


class CalculationMeta(models.Model):
    """Модель мета-данных расчета."""

    calculation_number = models.PositiveIntegerField(
        verbose_name="Номер расчета", unique=True, null=True, blank=True
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата расчета", auto_now_add=True
    )

    class Meta:
        """Мета-данные модели CalculationMeta."""

        verbose_name = "Мета-данные расчета"
        verbose_name_plural = "Мета-данные расчетов"

    def __str__(self):
        """
        :return: Номер расчета.
        """

        return self.calculation_number


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
    factors = models.JSONField(
        verbose_name="Расчетные коэффициенты", null=True, blank=True
    )
    result_value = models.FloatField(verbose_name="Результат расчета")

    class Meta:
        """Мета-данные модели CalculationData."""

        verbose_name = "Протокол расчета"
        verbose_name_plural = "Протоколы расчетов"