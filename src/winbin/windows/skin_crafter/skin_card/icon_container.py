import tkinter
from PIL.Image import Image
from customtkinter import CTkFrame

from core.skin import Skin
from .icon_item import IconItem


class IconContainer(CTkFrame):
    def __init__(self, master, skin: Skin):
        super().__init__(
            master=master,
            corner_radius=7
        )

        self.__inner_frame = CTkFrame(
            master=self,
            fg_color="#cfcfcf"
        )
        self.__inner_frame.grid(row=0, column=0, padx=5, pady=5, ipadx=10, ipady=10)

        for light_icon, dark_icon in zip(skin.light_icons, skin.dark_icons):
            self.pack_icon(light_icon, dark_icon)

    def pack_icon(self, light_image: Image, dark_image: Image):
        icon_frame = IconItem(self.__inner_frame, light_image, dark_image)
        icon_frame.pack(side=tkinter.LEFT)