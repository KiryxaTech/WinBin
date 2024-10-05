import pythoncom
import threading
import time
from PIL.Image import Image
from pystray import Icon, Menu, MenuItem
from ooj import JsonFile

from core import IconPackage, RecycleBin, Size, SizeConverter


class BinIcon(Icon):
    def __init__(self, icons_package: IconPackage, recycle_bin: RecycleBin):
        super().__init__("WinBin")
        self._icons_package = icons_package
        self._recycle_bin = recycle_bin
        self._last_icon_index = None
        self._setup_menu()
        self.update_tray_data()
        self.start_background_update()

    def _setup_menu(self):
        """Creates the system tray icon menu."""
        self.menu = Menu(
            MenuItem("Open", self._recycle_bin.open_bin_in_explorer),
            MenuItem("Clear", self.clear, default=True),
            MenuItem("Exit", self.stop)
        )

    def clear(self):
        """Clears the recycle bin and updates tray data."""
        self._recycle_bin.clear_bin()
        self.update_tray_data()

    def update_icon(self, icon: Image) -> None:
        """Updates the system tray icon if it has changed."""
        if self.icon != icon:
            self.icon = icon

    def get_usage_percentage(self) -> float:
        """Returns the recycle bin usage percentage."""
        if self._recycle_bin.max_size > 0:
            return self._recycle_bin.total_size / self._recycle_bin.max_size
        return 0

    def update_tray_data(self) -> None:
        """Updates both the tray icon and title based on recycle bin status."""
        self.update_based_on_bin_size()
        self.update_title()

    def update_based_on_bin_size(self) -> None:
        """Updates the icon based on recycle bin usage."""
        usage_percentage = self.get_usage_percentage()
        num_icons = len(self._icons_package.images)

        if usage_percentage == 0:
            icon_index = 0
        elif usage_percentage >= 1:
            icon_index = num_icons - 1
        else:
            icon_index = int(usage_percentage * (num_icons - 2)) + 1

        if icon_index != self._last_icon_index:
            self._last_icon_index = icon_index
            self.update_icon(self._icons_package.images[icon_index])

    def update_title(self):
        """Updates the tray icon title based on recycle bin status."""
        size_bytes = self._recycle_bin.total_size
        size_max_unit = SizeConverter.convert_to_max_unit(Size(size_bytes, Size.B))

        max_size = self._recycle_bin.max_size
        max_size_max_unit = SizeConverter.convert_to_max_unit(Size(max_size, Size.B))

        percent = f"{int(size_bytes / max_size * 100)}%" if max_size > 0 else "0%"

        files_count = self._recycle_bin.item_count
        if files_count > 0:
            files_delete_placeholder = f"\n\nClick to delete {files_count} files"
        else:
            files_delete_placeholder = ""

        title = f"Recycle Bin | {size_max_unit} • {percent} • Max {max_size_max_unit}{files_delete_placeholder}"
        
        if title != self.title:
            self.title = title

    def _update_data(self):
        """Background process for updating recycle bin data."""
        pythoncom.CoInitialize()
        configurate_file = JsonFile(r"config\configurate.json")
        try:
            while True:
                self.update_tray_data()

                configurate_file.update_buffer_from_file()
                update_frequency = configurate_file.get_entry("update_frequency")
                time.sleep(update_frequency)
        finally:
            pythoncom.CoUninitialize()

    def start_background_update(self):
        """Starts background process for updating tray data."""
        threading.Thread(target=self._update_data, daemon=True).start()

    def stop(self):
        """Stops the tray icon and the program."""
        self.icon.visible = False
        super().stop()