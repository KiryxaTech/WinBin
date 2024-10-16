import tkinter

from customtkinter import CTkFrame, CTkLabel
from PIL import Image

from core.skin import Skin, SkinManager
from .button import SkinCardButton


class SkinCardBottom(CTkFrame):
    def __init__(
        self,
        master,
        skin: Skin
    ) -> None:
        
        super().__init__(
            master=master,
            height=30,
            fg_color="transparent"
        )

        self.__skin = skin

        self.__create_widgets()

    def __create_widgets(self):
        """Создаёт виджеты нижней части карточки."""
        self.__create_skin_name_label()
        self.__create_apply_button()
        self.__create_delete_button()

    def __create_skin_name_label(self):
        """Создаёт метку с названием скина."""
        self.skin_name_field = CTkLabel(
            master=self,
            text=self.__skin.name.capitalize(),
            font=("Segoe UI", 16),
            anchor="w"
        )
        self.skin_name_field.pack(side=tkinter.LEFT, padx=(10, 0))

    def __create_apply_button(self):
        """Создаёт кнопку применения скина."""
        self.apply_button = SkinCardButton(
            master=self,
            icon_name="apply",
            action=self.__apply_skin,
            active_color="#37B9F3",
            hover_color="#2B92C0",
            press_color="#33AFE6",
            disable_color="#1A6287",
            is_disable=True
        )
        self.apply_button.right_pack()

    def __create_delete_button(self):
        icon = Image.open("assets/delete.png")

        self.delete_button = SkinCardButton(
            master=self,
            icon_name="delete",
            action=self.__delete_skin,
            active_color="#C71B1B",
            hover_color="#AC0909",
            press_color="#EA2E2E",
            disable_color="#A10000",
            is_disable=False
        )
        self.delete_button.right_pack()

    def __apply_skin(self):
        """Метод для применения скина."""
        SkinManager.set_default_skin(self.__skin.name)

    def __delete_skin(self):
        SkinManager.remove_skin(self.__skin.name)
        print("Скин удалён!")
        self.master.destroy()