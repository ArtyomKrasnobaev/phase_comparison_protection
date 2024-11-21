from math import sqrt
from typing import Callable, Dict

from calculation.models import CalculationProtocol
from core.models import Component, Line


class CalculationService:
    """Сервис расчета параметров настройки ДФЗ."""

    def __init__(self, line: Line, k1=1.3, k2=0.9, k3=1.4) -> None:

        self.line = line
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.components = line.protection_device.components.all()
        self.CALCULATION_MAP: Dict[str, Callable[[Component], None]] = {
            "IЛ БЛОК": self.calculate_il_block,
            "IЛ ОТКЛ": self.calculate_il_break,
        }

    def save_result_to_db(self, component: Component, result_value: float) -> None:
        CalculationProtocol.objects.create(
            line=self.line, component=component, result_value=result_value
        )

    def get_calculation_function(
        self, component: Component
    ) -> Callable[[Component], None]:
        calculation_function = self.CALCULATION_MAP.get(component.setting_designation)
        return calculation_function

    def calculate_il_block(self, component: Component) -> None:
        il_block = sqrt(3) * self.k1 / self.k2 * self.line.current_capacity
        self.save_result_to_db(component, il_block)

    def calculate_il_break(self, component: Component) -> None:
        il_break = self.k3 * sqrt(3) * self.k1 / self.k2 * self.line.current_capacity
        self.save_result_to_db(component, il_break)

    def run(self):
        for component in self.components:
            calculation_function = self.get_calculation_function(component)
            if calculation_function:
                calculation_function(component)
            else:
                print(f"Для органа {component} нет расчетной функции")
