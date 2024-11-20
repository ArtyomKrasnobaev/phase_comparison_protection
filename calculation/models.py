from django.db import models

from core.models import Component, Line


class CalculationProtocol(models.Model):
    """Модель протокола расчета параметров настройки ДФЗ."""

    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    condition = models.CharField(verbose_name="Расчетное условие", max_length=100)
    result_value = models.FloatField(verbose_name="Уставка")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Мета-данные модели CalculationProtocol."""

        verbose_name = "Протокол расчета"
        verbose_name_plural = "Протоколы расчетов"
