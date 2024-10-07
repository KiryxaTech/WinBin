import win32api
import win32gui
import threading
import time
import darkdetect

class ThemeTracker:
    def __init__(self, action: callable) -> None:
        self.__action = action
        self.__tracking = False
        self.__stop_event = threading.Event()
        self.__previous_theme = None

    def __monitor_theme(self):
        while not self.__stop_event.is_set():
            current_theme = darkdetect.theme()

            if self.__previous_theme is None:
                self.__previous_theme = current_theme

            if current_theme != self.__previous_theme:
                self.__action()
                self.__previous_theme = current_theme

            time.sleep(1)

    def start_tracking(self) -> None:
        """Запускает отслеживание изменений темы."""
        if not self.__tracking:
            self.__tracking = True
            self.__stop_event.clear()
            self.__thread = threading.Thread(target=self.__monitor_theme, daemon=True)
            self.__thread.start()

    def stop_tracking(self) -> None:
        """Останавливает отслеживание изменений темы."""
        if self.__tracking:
            self.__stop_event.set()
            self.__thread.join()
            self.__tracking = False
            print("Отслеживание темы остановлено.")