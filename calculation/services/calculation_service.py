import math

from calculation.models import CalculationProtocol
from core.models import Line


class CalculationService:
    """Сервис расчета параметров настройки ДФЗ."""

    def __init__(self, line: Line) -> None:
        """Конструктор для передачи ЛЭП."""

        self.line = line

    def calculate_phase_current_difference_block(
        self, grading_factor: float, reset_factor: float
    ) -> float:
        """
        Рассчитывает уставку блокирующего органа с пуском по векторной
        разности фазных токов по условию отстройки от нагрузочных режимов.

        :param reset_factor: Коэффициент возврата органа устройства.
        :param grading_factor: Коэффициент отстройки от нагрузочных режимов.
        :return: Значение уставки блокирующего органа в Амперах.
        """

        circuit_factor = math.sqrt(3)
        phase_current_difference_block_result = (
            circuit_factor * grading_factor / reset_factor * self.line.current_capacity
        )
        return phase_current_difference_block_result

    @staticmethod
    def calculate_phase_current_difference_break(
        matching_factor: float, block_result: float
    ) -> float:
        """
        Рассчитывает уставку отключающего органа с пуском по векторной
        разности фазных токов по условию согласования с блокирующим органом.

        :param block_result: Уставка блокирующего органа.
        :param matching_factor: Коэффициент согласования с блокирующим органом.
        :return: Значение уставки отключающего органа в Амперах.
        """

        phase_current_difference_break_result = matching_factor * block_result
        return phase_current_difference_break_result

    def calculate_negative_sequence_current_block(
        self, grading_factor: float, imbalance_factor: float, reset_factor: float
    ) -> float:
        """
        Рассчитывает уставку блокирующего органа с пуском по току обратной
        последовательности по условию отстройки от тока небаланса.

        :param reset_factor: Коэффициент возврата органа устройства.
        :param grading_factor: Коэффициент отстройки от тока небаланса.
        :param imbalance_factor: Коэффициент небаланса.
        :return: Значение уставки блокирующего органа в Амперах.
        """

        imbalance_current = imbalance_factor * self.line.current_capacity
        negative_sequence_current_block_result = (
            grading_factor / reset_factor * imbalance_current
        )
        return negative_sequence_current_block_result

    @staticmethod
    def calculate_negative_sequence_current_break(
        matching_factor: float, block_result: float
    ) -> float:
        """
        Рассчитывает уставку отключающего органа с пуском по току обратной
        последовательности по условию согласования с блокирующим органом.

        :param matching_factor: Коэффициент согласования с блокирующим органом.
        :param block_result: Уставка блокирующего органа.
        :return: Значение уставки отключающего органа в Амперах.
        """

        negative_sequence_current_break_result = matching_factor * block_result
        return negative_sequence_current_break_result

    @staticmethod
    def calculate_negative_sequence_voltage_block(
        grading_factor: float,
        reset_factor: float,
        imbalance_voltage: float,
        transformer_factor: float,
    ) -> float:
        """
        Рассчитывает уставку блокирующего органа с пуском
        по напряжению обратной последовательности по
        условию отстройки от напряжения небаланса.

        :param grading_factor: Коэффициент отстройки от напряжения небаланса.
        :param reset_factor: Коэффициент возврата органа устройства.
        :param imbalance_voltage: Напряжение небаланса в В.
        :param transformer_factor: Коэффициент трансформации ТН.
        :return: Значение уставки блокирующего органа в кВ.
        """

        negative_sequence_voltage_block_result = (
            grading_factor / reset_factor * (imbalance_voltage * transformer_factor)
        ) / 1000
        return negative_sequence_voltage_block_result

    @staticmethod
    def calculate_negative_sequence_voltage_break(
        matching_factor: float, block_result: float
    ) -> float:
        """
        Рассчитывает уставку отключающего органа с пуском
        по напряжению обратной последовательности по
        условию согласования с блокирующим органом.

        :param matching_factor: Коэффициент согласования с блокирующим органом.
        :param block_result: Уставка блокирующего органа в кВ.
        :return: Значение уставки отключающего органа в кВ.
        """

        negative_sequence_voltage_break_result = matching_factor * block_result
        return negative_sequence_voltage_break_result

    def save_result_to_db(self, component: str, condition: str, result: float) -> None:
        """Функция сохранения результатов расчета в БД."""

        CalculationProtocol.objects.create(
            line=self.line,
            component=component,
            condition=condition,
            result_value=result,
        )

    def execute_all_calculations(self, **kwargs) -> None:
        """
        Выполняет все расчеты уставок и сохраняет результаты в БД.

        Принимает параметры для отдельных методов через `kwargs`.
        """

        # Расчет блокирующего органа по фазным токам
        block_phase_result = self.calculate_phase_current_difference_block(
            grading_factor=kwargs["grading_factor"],
            reset_factor=kwargs["reset_factor"],
        )
        self.save_result_to_db(
            component="Фазные токи (Блокирующий)",
            condition="Отстройка от нагрузочных режимов",
            result=block_phase_result,
        )

        # Расчет отключающего органа по фазным токам
        trip_phase_result = self.calculate_phase_current_difference_break(
            matching_factor=kwargs["matching_factor"],
            block_result=block_phase_result,
        )
        self.save_result_to_db(
            component="Фазные токи (Отключающий)",
            condition="Согласование с блокирующим органом",
            result=trip_phase_result,
        )

        # Расчет блокирующего органа по току обратной последовательности
        block_negative_current_result = self.calculate_negative_sequence_current_block(
            grading_factor=kwargs["grading_factor"],
            imbalance_factor=kwargs["imbalance_factor"],
            reset_factor=kwargs["reset_factor"],
        )
        self.save_result_to_db(
            component="Ток обратной последовательности (Блокирующий)",
            condition="Отстройка от тока небаланса",
            result=block_negative_current_result,
        )

        # Расчет отключающего органа по току обратной последовательности
        trip_negative_current_result = self.calculate_negative_sequence_current_break(
            matching_factor=kwargs["matching_factor"],
            block_result=block_negative_current_result,
        )
        self.save_result_to_db(
            component="Ток обратной последовательности (Отключающий)",
            condition="Согласование с блокирующим органом",
            result=trip_negative_current_result,
        )

        # Расчет блокирующего органа по напряжению обратной последовательности
        block_negative_voltage_result = self.calculate_negative_sequence_voltage_block(
            grading_factor=kwargs["grading_factor"],
            reset_factor=kwargs["reset_factor"],
            imbalance_voltage=kwargs["imbalance_voltage"],
            transformer_factor=kwargs["transformer_factor"],
        )
        self.save_result_to_db(
            component="Напряжение обратной последовательности (Блокирующий)",
            condition="Отстройка от напряжения небаланса",
            result=block_negative_voltage_result,
        )

        # Расчет отключающего органа по напряжению обратной последовательности
        trip_negative_voltage_result = self.calculate_negative_sequence_voltage_break(
            matching_factor=kwargs["matching_factor"],
            block_result=block_negative_voltage_result,
        )
        self.save_result_to_db(
            component="Напряжение обратной последовательности (Отключающий)",
            condition="Согласование с блокирующим органом",
            result=trip_negative_voltage_result,
        )
