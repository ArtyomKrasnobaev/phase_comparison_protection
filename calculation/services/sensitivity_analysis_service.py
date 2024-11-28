from calculation.models import *
from core.models import Component


class SensitivityAnalysisService:
    """Сервис анализа чувствительности."""

    def __init__(
            self,
            calculation_meta: CalculationMeta
    ) -> None:

        self.calculation_meta = calculation_meta
        self.settings_calculation_protocols = (
            SettingsCalculationProtocol.objects.filter(
                calculation_meta=self.calculation_meta
            )
        )

        # Маппинг органов и видов КЗ
        self.FAULT_TYPE_MAP = {
            'IЛ ОТКЛ': ['Трехфазное КЗ'],
            'I2 ОТКЛ': ['Двухфазное КЗ', 'Двухфазное КЗ на землю', 'Однофазное КЗ'],
            'DI2 ОТКЛ': ['Двухфазное КЗ', 'Двухфазное КЗ на землю', 'Однофазное КЗ']
        }

    @staticmethod
    def save_result_to_db(
            settings_calculation_protocol: SettingsCalculationProtocol,
            fault_calculation_protocol: FaultCalculationProtocol,
            sensitivity_rate: float
    ) -> None:

        SensitivityAnalysisProtocol.objects.create(
            settings_calculation_protocol=settings_calculation_protocol,
            fault_calculation_protocol=fault_calculation_protocol,
            sensitivity_rate=sensitivity_rate
        )

    def get_fault_types(self, component: Component):
        fault_type = self.FAULT_TYPE_MAP.get(component.setting_designation)
        return fault_type

    @staticmethod
    def calculate_sensitivity(
            fault_protocol: FaultCalculationProtocol,
            component: Component,
            result_value: float
    ) -> float:
        fault_current_map = {
            'IЛ ОТКЛ': fault_protocol.positive_sequence_current,
            'I2 ОТКЛ': fault_protocol.negative_sequence_current,
            'DI2 ОТКЛ': fault_protocol.negative_sequence_current
        }
        fault_current = fault_current_map.get(component.setting_designation)
        sensitivity_rate = fault_current / result_value
        return sensitivity_rate

    def run(self):
        print("Выполняется анализ чувствительности...")

        for setting_calculation_protocol in self.settings_calculation_protocols:
            print(f"Обработка протокола {setting_calculation_protocol}.")
            component = setting_calculation_protocol.component
            fault_types = self.get_fault_types(component)

            if fault_types:
                print(f"\tОрган: {component.setting_designation}, Виды КЗ: {fault_types}")

                for fault_type in fault_types:
                    fault_protocols = FaultCalculationProtocol.objects.filter(
                        fault_type=fault_type,
                        protection_half_set=setting_calculation_protocol.protection_half_set
                    )
                    print(f"\t{fault_type}, найдено {fault_protocols.count()} протоколов расчета КЗ")

                    for fault_protocol in fault_protocols:
                        sensitivity_rate = self.calculate_sensitivity(
                            fault_protocol=fault_protocol,
                            component=component,
                            result_value=setting_calculation_protocol.result_value
                        )
                        print(f"\tКоэффициент чувствительности: {sensitivity_rate:.2f}")

                        self.save_result_to_db(
                            settings_calculation_protocol=setting_calculation_protocol,
                            fault_calculation_protocol=fault_protocol,
                            sensitivity_rate=round(sensitivity_rate, 2)
                        )
            else:
                print(f'\tДля органа {component} не найдены расчетные виды КЗ.')

        print("Анализ чувствительности завершен.")