# KiryxaTech 2024, MIT License

import customtkinter as ctk
from core.skin import Skin, SkinManager

class SkinPreviewWidget(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master,
            height=200
        )

        self.preview_field = ctk.CTkFrame()