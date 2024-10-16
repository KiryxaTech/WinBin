import threading
import win32api
import win32con


class ThemeController:
    def __init__(self, action: callable) -> None:
        self.__action = action
        self.__stop_event = threading.Event()

        self.previous_theme = self.get_current_theme()

    def get_current_theme(self) -> str:
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize')
        value, _ = win32api.RegQueryValueEx(key, "SystemUsesLightTheme")
        win32api.RegCloseKey(key)
        return "light" if value == 1 else "dark"

    def __monitor_theme(self):
        while not self.__stop_event.is_set():
            current_theme = self.get_current_theme()

            if current_theme != self.previous_theme:
                self.__action()
                self.previous_theme = current_theme

            self.__stop_event.wait(1)

    def start_tracking(self) -> None:
        self.__stop_event.clear()
        self.__thread = threading.Thread(target=self.__monitor_theme, daemon=True)
        self.__thread.start()

    def stop_tracking(self) -> None:
        self.__stop_event.set()
        self.__thread.join()