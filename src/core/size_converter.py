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

    def __init__(self, value: float, unit: SIZES):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"{self.value} {self.unit}"


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


# Пример использования
size_in_mb = Size(1024, Size.MB)
size_in_gb = SizeConverter.convert(size_in_mb, Size.GB)

print(f"{size_in_mb} = {size_in_gb} GB")  # Ожидается: 1024 MB = 1 GB