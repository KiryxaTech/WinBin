# KiryxaTech 2024, MIT License

import tkinter as tk

import customtkinter as ctk

from core.loader import ImageLoader, ThemedPack


class CollapsibleWidget(ctk.CTkFrame):
    def __init__(
            self,
            master,
            icon: ThemedPack,
            text: str,
            # description: str,
            internal_widget: ctk.CTkFrame
        ) -> None:
        """  """

        super().__init__(
            master=master,
            fg_color=("#eaeaea", "#2d2d2d")
        )

        self.image_widget = ctk.CTkLabel(
            master=self,
            width=40,
            height=40,
            image=ctk.CTkImage(
                light_image=icon.light,
                dark_image=icon.dark,
                size=(25, 25)
            ),
            fg_color="transparent",
            text=None
        )
        self.image_widget.pack(side=tk.LEFT, padx=(15, 0), pady=10)

        self.text_widget = ctk.CTkLabel(
            master=self,
            height=40,
            fg_color="transparent",
            text=text,
            text_color="white",
            font=("Gotham", 14)
        )
        self.text_widget.pack(side=tk.LEFT, padx=(15, 0))

        chevron_down = ImageLoader.get_ctk_image("regular.chevronDown", 18)
        chevron_down = ImageLoader.get_ctk_image("regular.chevronUp", 18)
        self.arrow_widget = ctk.CTkLabel(
            master=self,
            width=40,
            height=40,
            image=chevron_down,
            fg_color="transparent",
            text=None
        )
        self.arrow_widget.pack(side=tk.RIGHT, padx=(0, 15))