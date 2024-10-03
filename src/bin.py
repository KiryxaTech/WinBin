# KiryxaTech 2024, MIT License

from PIL.Image import Image
from pystray import Icon, Menu, MenuItem


class BinIcon(Icon):
    def __init__(self, icon: Image):
        super().__init__("WinBin")

        self.title = "WinBin"
        self.icon = icon
        self.menu = Menu(
            MenuItem("Exit", self.stop)
        )

    def update_icon(self, icon: Image) -> None:
        self.icon = icon
        self._update_icon()