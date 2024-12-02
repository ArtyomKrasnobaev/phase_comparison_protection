from math import sqrt
from typing import Callable

from calculation.models import (CalculationMeta, FaultCalculation,
                                SettingsCalculation)
from core.models import Component, ProtectionHalfSet


class SettingsCalculationService:

    def __init__(
        self,
        calculation_meta: CalculationMeta,
        il_grading_factor=1.3,
        il_reset_factor=0.9,
        il_matching_factor=1.4,
        i2_imbalance_factor=0.05,
        i2_grading_factor=1.3,
        i2_reset_factor=0.9,
        i2_matching_factor=1.4,
        di1_matching_factor=1.4,
        u2_grading_factor=1.3,
        u2_reset_factor=0.9,
        u2_imbalance_voltage=1.5,
        voltage_transformer_factor=5000,
        u2_matching_factor=2.0,
    ) -> None:

        # Определяем коэффициенты для всех органов
        self.il_grading_factor = il_grading_factor
        self.il_reset_factor = il_reset_factor
        self.il_matching_factor = il_matching_factor
        self.i2_imbalance_factor = i2_imbalance_factor
        self.i2_grading_factor = i2_grading_factor
        self.i2_reset_factor = i2_reset_factor
        self.i2_matching_factor = i2_matching_factor
        self.di1_matching_factor = di1_matching_factor
        self.u2_grading_factor = u2_grading_factor
        self.u2_reset_factor = u2_reset_factor
        self.u2_matching_factor = u2_matching_factor
        self.u2_imbalance_voltage = u2_imbalance_voltage
        self.voltage_transformer_factor = voltage_transformer_factor

        # Определяем мета-данные расчета
        self.calculation_meta = calculation_meta

        # Определяем линию и полукомплекты защиты
        self.line = calculation_meta.line
        self.protection_half_sets = self.line.protection_half_sets.all()

        # Карта расчетных функций органов
        self.CALCULATION_MAP = {
            "IЛ БЛОК": self.calculate_il_block,
            "IЛ ОТКЛ": self.calculate_il_break,
            "I2 БЛОК": self.calculate_i2_block,
            "I2 ОТКЛ": self.calculate_i2_break,
            'DI1 БЛОК': self.calculate_di1_block,
            'DI1 ОТКЛ': self.calculate_di1_break,
            "DI2 БЛОК": self.calculate_i2_block,
            "DI2 ОТКЛ": self.calculate_i2_break,
            "U2 БЛОК": self.calculate_u2_block,
            "U2 ОТКЛ": self.calculate_u2_break,
        }

        self.di1_sensitivity_rate = 2

    def save_result_to_db(
        self,
        protection_half_set: ProtectionHalfSet,
        component: Component,
        result_value: float,
    ) -> None:
        SettingsCalculation.objects.create(
            calculation_meta=self.calculation_meta,
            protection_half_set=protection_half_set,
            component=component,
            result_value=result_value,
        )

    def get_calculation_function(self, component: Component) -> Callable[[], float]:
        calculation_function = self.CALCULATION_MAP.get(component.setting_designation)
        return calculation_function

    def calculate_il_block(self) -> float:
        il_block_value = (
            sqrt(3)
            * self.il_grading_factor
            / self.il_reset_factor
            * self.line.current_capacity
        )
        return il_block_value

    def calculate_il_break(self) -> float:
        il_break_value = round(self.il_matching_factor * self.calculate_il_block(), 2)
        return il_break_value

    def calculate_di1_break(self) -> float:
        fault_calculations = FaultCalculation.objects.filter(
            protection_half_set__in=self.protection_half_sets,
            fault_type='К(3)'
        )

        i1_values = []
        for fault_calculation in fault_calculations:
            i1_values.append(fault_calculation.fault_values.get('I1'))

        min_i1 = min(i1_values)
        di1_break_value = min_i1 / self.di1_sensitivity_rate
        return di1_break_value

    def calculate_di1_block(self) -> float:
        di1_break_value = self.calculate_di1_break()
        di1_block_value = di1_break_value / self.di1_matching_factor
        return di1_block_value

    def calculate_i2_block(self) -> float:
        i2_imbalance_current = self.i2_imbalance_factor * self.line.current_capacity
        i2_block_value = (
            self.i2_grading_factor / self.i2_reset_factor * i2_imbalance_current
        )
        return i2_block_value

    def calculate_i2_break(self) -> float:
        i2_break_value = self.i2_matching_factor * self.calculate_i2_block()
        return i2_break_value

    def calculate_u2_block(self) -> float:
        u2_block_value = (
            self.u2_grading_factor
            / self.u2_reset_factor
            * (self.u2_imbalance_voltage * self.voltage_transformer_factor)
            / 1000
        )
        return u2_block_value

    def calculate_u2_break(self) -> float:
        u2_break_value = self.u2_matching_factor * self.calculate_u2_block()
        return u2_break_value

    def run(self) -> None:
        print(f'Выполняем расчет параметров настройки ДФЗ {self.calculation_meta.line}')
        for protection_half_set in self.protection_half_sets:
            print(f'\tВыполняем расчет параметров настройки полукомплекта {protection_half_set}')
            components = protection_half_set.protection_device.components.all()
            for component in components:
                calculation_function = self.get_calculation_function(component)
                if calculation_function:
                    print(
                        f"\tРасчет параметров настройки органа {component}"
                    )
                    result = round(calculation_function(), 0)
                    self.save_result_to_db(protection_half_set, component, result)
                else:
                    print(f"\tОтсутствует расчетный модуль для органа {component}")
        print(f'Расчет параметров настройки {self.calculation_meta.line} завершен')