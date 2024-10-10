from customtkinter import CTkFrame, CTkLabel, CTkImage
from PIL.Image import Image


class IconItem(CTkFrame):
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