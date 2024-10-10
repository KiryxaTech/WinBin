import tkinter
from PIL.Image import Image
from customtkinter import CTkFrame, CTkLabel, CTkImage

from core.skin import Skin


class IconFrame(CTkFrame):
    def __init__(self, master, light_image: Image, dark_image: Image):
        super().__init__(
            master=master,
            width=50,
            height=50,
            corner_radius=7
        )

        self.__icon_label = CTkLabel(
            master=self,
            image=CTkImage(
                light_image=dark_image,
                dark_image=light_image,
                size=(50, 50),
            ),
            text="",
            fg_color="#cfcfcf"
        )
        self.__icon_label.place(x=0, y=0)


class IconBoxWidget(CTkFrame):
    def __init__(self, master, skin: Skin):
        super().__init__(
            master=master,
            corner_radius=7
        )

        self.__inner_frame = CTkFrame(
            master=self,
            fg_color="#cfcfcf"
        )
        self.__inner_frame.grid(row=0, column=0, padx=5, pady=5)

        for light_icon, dark_icon in zip(skin.light_icons, skin.dark_icons):
            self.pack_icon(light_icon, dark_icon)

    def pack_icon(self, light_image: Image, dark_image: Image):
        icon_frame = IconFrame(self.__inner_frame, light_image, dark_image)
        icon_frame.pack(side=tkinter.LEFT)