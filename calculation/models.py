from django.db import models

from core.models import Line


class CalculationProtocol(models.Model):
    """Модель протокола расчета параметров настройки ДФЗ."""

    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    component = models.CharField(verbose_name="Орган", max_length=100)
    condition = models.CharField(verbose_name="Расчетное условие", max_length=100)
    result_value = models.FloatField(verbose_name="Значение уставки")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Мета-данные модели CalculationProtocol."""

        verbose_name = "Протокол расчета"
        verbose_name_plural = "Протоколы расчетов"

    def __str__(self):
        """Возвращает ЛЭП, орган, величину уставки и метку времени."""

        formatted_time = self.timestamp.strftime("%d.%m.%Y %H:%M:%S")
        protocol = f"{self.line}, {self.component}, {self.condition}, {self.result_value:.2f}, {formatted_time}"
        return protocol
