import win32com.client
import ctypes
import winreg
import os

from core.size_converter import Size, SizeConverter

# Структура для хранения информации о корзине
class SHQUERYRBINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_ulong),
        ('i64Size', ctypes.c_longlong),
        ('i64NumItems', ctypes.c_longlong),
    ]


class RecycleBin:
    RECYCLE_BIN_NAMESPACE = 10
    BITBUCKET_KEY_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\BitBucket"

    def __init__(self, drive_letter="C:"):
        self.drive_letter = drive_letter

    @property
    def size(self) -> int:
        """Возвращает общий размер файлов в корзине."""
        return self._calculate_bin_size()

    @property
    def files_count(self) -> int:
        """Возвращает количество файлов в корзине."""
        info = self._get_recycle_bin_info()
        return info.get('num_items', 0) if info else 0

    @property
    def max_size(self) -> int:
        """Возвращает максимальный размер корзины в байтах."""
        return self._get_recycle_bin_max_size()

    def set_recycle_bin_max_size(self, size_in_bytes: int) -> None:
        """Устанавливает максимальный размер корзины для указанного диска."""
        size_in_mb = SizeConverter.convert(Size(size_in_bytes, Size.B), Size.MB)
        self._update_max_capacity_in_registry(size_in_mb)

    def _calculate_bin_size(self) -> int:
        """Внутренний метод для вычисления общего размера файлов в корзине."""
        shell = win32com.client.Dispatch("Shell.Application")
        recycle_bin = shell.NameSpace(self.RECYCLE_BIN_NAMESPACE)
        total_size = 0

        def get_item_size(item):
            nonlocal total_size
            if item.IsFolder:
                folder = shell.NameSpace(item.Path)
                for sub_item in folder.Items():
                    get_item_size(sub_item)
            else:
                total_size += item.Size

        for item in recycle_bin.Items():
            get_item_size(item)

        return total_size

    def _get_recycle_bin_info(self):
        """Получает информацию о корзине, используя SHQueryRecycleBinW."""
        SHQueryRecycleBin = ctypes.windll.shell32.SHQueryRecycleBinW

        rb_info = SHQUERYRBINFO()
        rb_info.cbSize = ctypes.sizeof(SHQUERYRBINFO)
        recycle_bin_path = f"{self.drive_letter}\\"

        result = SHQueryRecycleBin(recycle_bin_path, ctypes.byref(rb_info))
        if result == 0:  # S_OK
            return {"size_in_bytes": rb_info.i64Size, "num_items": rb_info.i64NumItems}
        return None

    def _get_recycle_bin_max_size(self) -> int:
        """Получает максимальный размер корзины из реестра для данного диска."""
        try:
            bitbucket_guid = self._get_last_enum_guid()
            volume_key_path = os.path.join(self.BITBUCKET_KEY_PATH, "Volume", bitbucket_guid)
            return self._get_max_capacity_from_registry(volume_key_path)
        except OSError:
            return 0

    def _update_max_capacity_in_registry(self, size_in_mb: int) -> None:
        """Обновляет значение MaxCapacity для указанного диска в реестре."""
        try:
            bitbucket_guid = self._get_last_enum_guid()
            volume_key_path = os.path.join(self.BITBUCKET_KEY_PATH, "Volume", bitbucket_guid)
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, volume_key_path, 0, winreg.KEY_WRITE) as volume_key:
                winreg.SetValueEx(volume_key, "MaxCapacity", 0, winreg.REG_DWORD, size_in_mb)
        except OSError:
            print("Ошибка доступа к реестру.")

    def _get_last_enum_guid(self) -> str:
        """Получает GUID последнего тома из ключа реестра."""
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.BITBUCKET_KEY_PATH) as bitbucket_key:
            last_enum, _ = winreg.QueryValueEx(bitbucket_key, "LastEnum")
            return last_enum[0].split(",")[1]

    def _get_max_capacity_from_registry(self, volume_key_path: str) -> int:
        """Возвращает максимальный размер корзины в мегабайтах из реестра."""
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, volume_key_path) as volume_key:
            max_size_mb, _ = winreg.QueryValueEx(volume_key, "MaxCapacity")
            return SizeConverter.convert(Size(max_size_mb, Size.MB), Size.B)

    @staticmethod
    def _convert_bytes_to_mb(size_in_bytes: int) -> int:
        """Конвертирует байты в мегабайты."""
        return size_in_bytes // (1024 * 1024)