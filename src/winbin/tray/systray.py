# KiryxaTech 2024, MIT License

import os
from threading import Thread
from typing import Literal

import darkdetect
from PIL.Image import Image
from pystray import Icon as Icon, Menu, MenuItem

from core.recycle_bin import RecycleBin, SizeController
from core.size_converter import Size, SizeConverter
from core.skin import Skin
from core.theme_controller import ThemeController
from winbin.windows import SkinCrafterWindow


class IconUpdater:
    """
    Responsible for updating the tray icon based on the current theme and recycle bin fullness level.
    """
    def __init__(self, tray_icon: 'TrayIcon', skin: Skin):
        """
        Initializes the IconUpdater with the tray icon and the current skin.

        Args:
            tray_icon (TrayIcon): The system tray icon object.
            skin (Skin): The skin object that contains icon sets for different themes.
        """
        self._tray_icon = tray_icon
        self._current_skin = skin
        self._previous_icon_index = 0
        self._previous_theme: Literal["Light", "Dark"] = darkdetect.theme()

    def update_icon(self):
        """
        Updates the tray icon according to the current theme (Light or Dark).
        """
        current_theme = darkdetect.theme()
        icons = self._get_icons_for_theme(current_theme)
        icon = icons[self._previous_icon_index]
        self._tray_icon.set_icon(icon)

    def update_level(self, percent_fullness: float):
        """
        Updates the tray icon based on the recycle bin's fullness level.

        Args:
            percent_fullness (float): The current fullness of the recycle bin as a percentage.
        """
        icons = self._get_icons_for_theme(self._previous_theme)
        icon = self._select_icon_by_fullness(icons, percent_fullness)
        self._previous_icon_index = icons.index(icon)
        self._tray_icon.set_icon(icon)

    def _get_icons_for_theme(self, theme: Literal["Light", "Dark"]) -> list:
        """
        Returns the set of icons for the specified theme.

        Args:
            theme (Literal["Light", "Dark"]): The current theme ("Light" or "Dark").

        Returns:
            list: A list of icons corresponding to the current theme.
        """
        return self._current_skin.dark_icons if theme == "Light" else self._current_skin.light_icons

    def _select_icon_by_fullness(self, icons: list, percent_fullness: float) -> Image:
        """
        Selects the appropriate icon from the icon set based on the recycle bin's fullness level.

        Args:
            icons (list): A list of icons for the current theme.
            percent_fullness (float): The current fullness of the recycle bin as a percentage.

        Returns:
            Image: The selected icon image based on fullness.
        """
        if percent_fullness <= 0:
            return icons[0]
        elif percent_fullness >= 1:
            return icons[-1]
        else:
            icon_index = int(percent_fullness * (len(icons) - 2)) + 1
            return icons[icon_index]


class TitleUpdater:
    """
    Updates the tray icon title with the current state of the recycle bin (size, fullness, etc.).
    """
    def __init__(self, tray_icon: 'TrayIcon', recycle_bin: RecycleBin):
        """
        Initializes the TitleUpdater with the tray icon and recycle bin.

        Args:
            tray_icon (TrayIcon): The system tray icon object.
            recycle_bin (RecycleBin): The recycle bin object containing state and properties.
        """
        self._tray_icon = tray_icon
        self._recycle_bin = recycle_bin

    def update_title(self):
        """
        Updates the title of the tray icon to reflect the current state of the recycle bin.
        """
        title = self._generate_title()
        self._tray_icon.set_title(title)

    def _generate_title(self) -> str:
        """
        Generates a string to represent the current state of the recycle bin (size, fullness, and items).

        Returns:
            str: The generated title representing the current state of the recycle bin.
        """
        fullness = SizeConverter.convert_to_max_unit(Size(self._recycle_bin.total_size))
        max_fullness = SizeConverter.convert_to_max_unit(Size(self._recycle_bin.max_size))

        if fullness is None or max_fullness is None:
            raise ValueError("Error in calculating fullness or max fullness values.")

        percent_fullness = self._get_percent_fullness()
        sections = [
            f"{fullness}",
            f"{round(percent_fullness)}%",
            f"Max {max_fullness}"
        ]
        title_size_section = " • ".join(sections)

        title = f"Recycle Bin | {title_size_section}"
        files_count = self._recycle_bin.item_count
        if files_count > 0:
            title += f"\n\nClick to delete {files_count} files."

        return title

    def _get_percent_fullness(self) -> float:
        """
        Calculates the percentage of the recycle bin's fullness.

        Returns:
            float: The fullness of the recycle bin as a percentage.
        """
        total_size = self._recycle_bin.total_size
        max_size = self._recycle_bin.max_size
        return total_size / max_size * 100


class ChangeController:
    """
    Tracks changes in the recycle bin size and theme, and triggers updates accordingly.
    """
    def __init__(self, size_change_action: callable, theme_change_action: callable) -> None:
        """
        Initializes the ChangeController with the actions to be triggered on size and theme changes.

        Args:
            size_change_action (callable): A callback function that is called when the recycle bin size changes.
            theme_change_action (callable): A callback function that is called when the system theme changes.
        """
        self.__size_controller = SizeController(size_change_action)
        self.__theme_controller = ThemeController(theme_change_action)

    def start(self):
        """
        Starts tracking size and theme changes.
        """
        self.__size_controller.start_tracking()
        self.__theme_controller.start_tracking()

    def stop(self):
        """
        Stops tracking size and theme changes.
        """
        self.__size_controller.stop_tracking()
        self.__theme_controller.stop_tracking()


APP_NAME = "WinBin"


class TrayIcon(Icon):
    """
    Represents the system tray icon for the WinBin application, with menu options and dynamic updates.
    """
    def __init__(self, skin: Skin, recycle_bin: RecycleBin) -> None:
        """
        Initializes the TrayIcon with the specified skin and recycle bin state.

        Args:
            skin (Skin): The skin object that contains icon sets for different themes.
            recycle_bin (RecycleBin): The recycle bin object containing state and properties.
        """

        super().__init__(APP_NAME)

        self.__recycle_bin = recycle_bin
        self.__icon_updater = IconUpdater(self, skin)
        self.__title_updater = TitleUpdater(self, recycle_bin)

        self.__change_controller = ChangeController(
            size_change_action=self.update_level_and_title,
            theme_change_action=self.update_theme
        )

        self.__setup_menu()
        self.update_theme()
        self.update_level_and_title()

    def set_skin(self, new_skin: Skin):
        """
        Changes the current skin and updates the tray icon accordingly.

        Args:
            new_skin (Skin): The new skin object containing icon sets for different themes.
        """

        self.__icon_updater = IconUpdater(self, new_skin)
        self.update_theme()

    def start(self) -> None:
        """
        Starts the tray icon in a separate thread and begins tracking changes.
        """

        self.__main_thread = Thread(target=super().run)
        self.__main_thread.start()
        self.__change_controller.start()

    def stop(self) -> None:
        """
        Stops tracking changes and exits the application.
        """

        self.__change_controller.stop()
        super().stop()
        os._exit(0)  # Stop all program processing.

    def update_level_and_title(self):
        """
        Updates both the icon and title based on the recycle bin's fullness.
        """

        percent_fullness = self.__title_updater._get_percent_fullness() / 100
        self.__icon_updater.update_level(percent_fullness)
        self.__title_updater.update_title()

    def update_theme(self):
        """
        Updates the tray icon according to the current theme (Light or Dark).
        """

        self.__icon_updater.update_icon()

    def set_icon(self, icon: Image):
        """
        Sets the tray icon image.

        Args:
            icon (Image): The image to be used as the tray icon.
        """

        self._icon = icon
        self._update_icon()

    def set_title(self, title: str):
        """
        Sets the tray icon's title.

        Args:
            title (str): The title to display when hovering over the tray icon.
        """

        self._title = title
        self._update_title()

    def __setup_menu(self):
        """
        Sets up the system tray menu with options for interacting with the recycle bin and application.
        """
        
        self.menu = Menu(
            MenuItem(
                text="Skin Crafter",
                action=SkinCrafterWindow
            ),
            MenuItem(
                text="Open",
                action=self.__recycle_bin.open_bin_in_explorer,
                default=True
            ),
            MenuItem(
                text="Empty",
                action=self.__recycle_bin.clear_bin
            ),
            Menu.SEPARATOR,
            MenuItem(
                text="Settings",
                action=None,
                enabled=False
            ),
            MenuItem(
                text="Add to startup",
                action=None,
                checked=None,
                enabled=False
            ),
            Menu.SEPARATOR,
            MenuItem(
                text="Exit",
                action=self.stop
            )
        )