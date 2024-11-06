import tkinter as tk

from core.image_loader import ImageLoader

from .page import Page
from winbin.windows.settings.widgets import BinFullnessWidget, CollapsibleWidget


class SkinsCollapsibleWidget(CollapsibleWidget):
    def __init__(self, master) -> None:
        super().__init__(
            master=master,
            iconpack=ImageLoader.get_themed_pack("regular.skins"),
            title="Skins"
        )
        self.bind_inner_frame(tk.Frame(self))


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master=master,
            name="Home"
        )

        self.bin_fullness_widget = BinFullnessWidget(self)
        self.bin_fullness_widget.pack(side=tk.TOP, fill=tk.X, pady=(20, 0))

        self.skins_collapsible_widget = SkinsCollapsibleWidget(self)
        self.skins_collapsible_widget.pack(side=tk.TOP, fill=tk.X, pady=(15, 0))