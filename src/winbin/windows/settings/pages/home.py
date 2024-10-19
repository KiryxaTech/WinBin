import tkinter as tk

from .page import Page
from ..widgets import BinFullnessWidget, SkinPreviewWidget, CollapsibleWidget

import PIL.Image

class HomePage(Page):
    def __init__(self, master):
        super().__init__(
            master=master,
            name="Home"
        )

        self.bin_fullness_widget = BinFullnessWidget(self)
        self.bin_fullness_widget.pack(side=tk.TOP, fill=tk.X, pady=(20, 0))

        # self.skin_preview_widget = SkinPreviewWidget(self)
        # self.skin_preview_widget.pack(side=tk.TOP, fill=tk.X, pady=(15, 0))

        img = PIL.Image.open(r"assets\app.png")
        self.collaps = CollapsibleWidget(self, image=[img, img], text="Collaps", internal_widget=Page(self, ""))
        self.collaps.pack(side=tk.TOP, fill=tk.X, pady=(15, 0))