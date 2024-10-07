import time
from threading import Thread, Event

import pythoncom

from .recycle_bin import RecycleBin


class SizeTracker:
    def __init__(self, action: callable) -> None:
        """Инициализация отслеживателя изменений размера файлов.
        :param action: Функция, которая будет вызываться при изменении размера файлов
        """
        self.__action = action
        self.__tracking = False
        self.__stop_event = Event()
        self.__thread = None
        self.recycle_bin = RecycleBin()  # Инициализируем объект класса RecycleBin

    def __monitor_folder_size(self) -> None:
        """Основной метод для отслеживания изменений размера файлов в корзине."""
        previous_size = None

        pythoncom.CoInitialize()
        try:
            while not self.__stop_event.is_set():
                # Получаем текущий размер корзины через метод твоего класса RecycleBin
                current_size = self.recycle_bin.total_size

                if previous_size is None:
                    previous_size = current_size

                if current_size != previous_size:
                    self.__action()  # Выполняем действие при изменении размера корзины
                    previous_size = current_size

                time.sleep(1)  # Задержка между проверками
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            pythoncom.CoUninitialize()

    def start_tracking(self) -> None:
        """Запускает отслеживание изменений размера файлов в корзине."""
        if not self.__tracking:
            self.__tracking = True
            self.__stop_event.clear()
            self.__thread = Thread(target=self.__monitor_folder_size, daemon=True)
            self.__thread.start()

    def stop_tracking(self) -> None:
        """Останавливает отслеживание изменений размера файлов."""
        if self.__tracking:
            self.__stop_event.set()
            self.__thread.join()
            self.__tracking = False
            print("Отслеживание размера мусорной корзины остановлено.")