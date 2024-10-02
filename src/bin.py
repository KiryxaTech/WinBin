# KiryxaTech 2024, MIT License

import PIL.Image
from pystray import Icon, Menu, MenuItem


class Bin(Icon):
    def __init__(self):
        super().__init__("WinBin")

        self.title = "WinBin"
        self.icon = PIL.Image.open("bin_3.png")
        self.menu = Menu(
            MenuItem("Exit", self.stop)
        )

    def update_icon(self, icon: PIL.Image) -> None:
        self.icon = icon
        self._update_icon()