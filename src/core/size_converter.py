from typing import Literal

# Тип, представляющий возможные единицы измерения размера
SIZES = Literal["B", "KB", "MB", "GB", "TB"]

class Size:
    """Класс, представляющий размер и единицу измерения."""
    
    B = "B"
    KB = "KB"
    MB = "MB"
    GB = "GB"
    TB = "TB"

    def __init__(self, value: float, unit: SIZES = B):
        self.value = value
        self.unit = unit

    def __repr__(self):
        if self.value % 1 == 0:
            return f"{int(self.value)} {self.unit}"
        return f"{self.value:.1f} {self.unit}".replace(".", ",")


class SizeConverter:
    """Класс для конвертации между различными единицами измерения размера."""
    
    UNITS_IN_BYTES = {
        Size.B: 1,
        Size.KB: 1024,
        Size.MB: 1024 ** 2,
        Size.GB: 1024 ** 3,
        Size.TB: 1024 ** 4
    }

    @staticmethod
    def convert(size: Size, target_unit: SIZES) -> float:
        """Конвертирует значение из одной единицы измерения в другую."""
        size_in_bytes = SizeConverter.convert_to_bytes(size)
        target_unit_in_bytes = SizeConverter.UNITS_IN_BYTES[target_unit]
        return size_in_bytes / target_unit_in_bytes

    @staticmethod
    def convert_to_bytes(size: Size) -> float:
        """Конвертирует размер в байты."""
        unit_in_bytes = SizeConverter.UNITS_IN_BYTES[size.unit]
        return size.value * unit_in_bytes
    
    @classmethod
    def convert_to_max_unit(cls, size: Size) -> Size:
        """Конвертирует размер в максимально возможную единицу измерения."""
        # Начальные значения
        current_value = size.value
        current_unit = size.unit

        units = [Size.B, Size.KB, Size.MB, Size.GB, Size.TB]
        # Перебираем возможные единицы измерения
        for i in range(len(units)):
            if current_value < 1024 or units[i] == Size.TB:  # Останавливаемся, если меньше 1024 или достигли TB
                break
            current_value /= 1024  # Делим на 1024 для перехода к следующей единице
            current_unit = units[i + 1]  # Обновляем единицу

        return Size(current_value, current_unit)  # Возвращаем новый объект Size