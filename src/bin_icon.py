from threading import Thread
from typing import Literal
import darkdetect
from PIL.Image import Image
from pystray import Icon as TrayIcon, Menu, MenuItem

from core.recycle_bin import RecycleBin, SizeTracker
from core.size_converter import Size, SizeConverter
from core.skin import Skin
from core.theme_tracker import ThemeTracker


class BinTrayIcon(TrayIcon):
    def __init__(
        self,
        skin: Skin,
        recycle_bin: RecycleBin
    ) -> None:
        
        super().__init__("WinBin")

        self.__skin = skin
        self.__recycle_bin = recycle_bin
        self.__size_tracker = SizeTracker(self.update_icon_level)
        self.__theme_tracker = ThemeTracker(self.update_icon_theme)

        self.__previous_icon_index = 0
        self.__previous_icon_theme: Literal["Light", "Dark"] = "Light"

        self.update_icon_level()
        self.update_icon_theme()
        self.update_title()
        self.create_menu()

    def run(self) -> None:
        self.__main_thread = Thread(target=super().run)
        self.__main_thread.start()

        self.__size_tracker.start_tracking()
        self.__theme_tracker.start_tracking()

    def stop(self) -> None:
        super().stop()
        
        self.__size_tracker.stop_tracking()
        self.__theme_tracker.stop_tracking()


    def create_menu(self):
        quit_item = MenuItem(
            text="Quit",
            action=self.stop
        )
        empty_bin_item = MenuItem(
            text="Empty",
            action=self.__recycle_bin.clear_bin,
            default=True
        )
        open_bin_item = MenuItem(
            text="Open in Explorer",
            action=self.__recycle_bin.open_bin_in_explorer
        )

        menu = Menu(open_bin_item, empty_bin_item, Menu.SEPARATOR, quit_item)

        menu = Menu(
            MenuItem(
                text="Open in explorer",
                action=self.__recycle_bin.open_bin_in_explorer
            ),
            MenuItem(
                text="Empty",
                action=self.__recycle_bin.clear_bin,
                default=True
            ),
            MenuItem(
                text="Quit",
                action=self.stop
            )
        )

        self.menu = menu

    def update_title(self) -> None:
        self._update_title(self._generate_title())

    def update_icon_level(self):
        if self.__previous_icon_theme == "Light":
            icons = self.__skin.light_icons
        else:
            icons = self.__skin.dark_icons

        percent_fullness = self.get_percent_fullness() / 100

        if percent_fullness <= 0:
            icon = icons[0]
        elif percent_fullness >= 1:
            icon = icons[-1]
        else:
            icons_count = len(icons)
            icon_index = int(percent_fullness * (icons_count - 2)) + 1
            icon = icons[icon_index]

        self.__previous_icon_index = icons.index(icon)
        self._update_icon(icon)

    def update_icon_theme(self):
        current_theme = darkdetect.theme()
        self.__previous_icon_theme = current_theme

        if current_theme == "Light":
            icons = self.__skin.dark_icons
        else:
            icons = self.__skin.light_icons

        icon = icons[self.__previous_icon_index]

        self._update_icon(icon)

    def _update_icon(self, icon: Image) -> None:
        self._icon = icon
        super()._update_icon()

    def _update_title(self, title: str) -> None:
        self.title = title
        super()._update_title()

    def _generate_title(self):
        fullness = SizeConverter.convert_to_max_unit(Size(self.__recycle_bin.total_size))
        max_fullness = SizeConverter.convert_to_max_unit(Size(self.__recycle_bin.max_size))

        if fullness is None or max_fullness is None:
            raise ValueError("Error in calculating fullness or max fullness values.")

        percent_fullness = self.get_percent_fullness()
        sections = [
            f"{fullness}",
            f"{round(percent_fullness)}%",
            f"Max {max_fullness}"
        ]
        title_size_section = " • ".join(sections)

        title = f"Recycle Bin | {title_size_section}"

        files_count = self.__recycle_bin.item_count
        if files_count > 0:
            title += f"\n\nClick to delete {files_count} files."

        return title

    def get_percent_fullness(self) -> float:
        total_size = self.__recycle_bin.total_size
        max_size = self.__recycle_bin.max_size

        return total_size / max_size * 100