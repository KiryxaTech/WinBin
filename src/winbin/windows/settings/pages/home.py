import tkinter

from .page import Page
from ..widgets import BinFullnessWidget


class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master=master,
            name="Home"
        )

        self.bin_fullness_widget = BinFullnessWidget(self)
        self.bin_fullness_widget.pack(side=tkinter.TOP, fill=tkinter.X, pady=(20, 0))