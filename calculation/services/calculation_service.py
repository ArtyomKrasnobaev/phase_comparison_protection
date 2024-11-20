from core.models import Line

from calculation.models import CalculationProtocol


class CalculationService:
    """Сервис расчета параметров настройки ДФЗ."""

    def __init__(self, line: Line):
        """Конструктор для передачи ЛЭП."""

        self.line = line

    def calculate_phase_current_difference_block(self, grading_rate: float, circuit_rate: float) -> float:
        """
        Функция расчета параметров настройки органа
        с пуском по векторной разности фазных токов.
        """

        result = circuit_rate * grading_rate * self.line.current_capacity
        return result

    def save_result_to_db(self, component: str, condition: str, result: float):
        """Функция сохранения результатов расчета в БД."""

        CalculationProtocol.objects.create(
            line=self.line,
            component=component,
            condition=condition,
            result_value=result
        )