# KiryxaTech 2024, MIT License

import tkinter as tk

import customtkinter as ctk
import PIL.Image
from PIL.Image import Image


class CollapsibleWidget(ctk.CTkFrame):
    def __init__(
            self,
            master,
            image: list[Image, Image],
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
                light_image=image[0],
                dark_image=image[1],
                size=(35, 35)
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
            font=("Gotham", 16)
        )
        self.text_widget.pack(side=tk.LEFT, padx=(15, 0))

        self.arrow_widget = ctk.CTkLabel(
            master=self,
            width=40,
            height=40,
            image=ctk.CTkImage(
                light_image=PIL.Image.open(r"assets\settings\ui\ChevronDownLight.png"),
                dark_image=PIL.Image.open(r"assets\settings\ui\ChevronDownDark.png"),
                size=(18, 18)
            ),
            fg_color="transparent",
            text=None
        )
        self.arrow_widget.pack(side=tk.RIGHT, padx=(0, 15))