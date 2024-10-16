import tkinter
from customtkinter import CTkFrame
from core.skin import Skin, SkinManager

from .icon_container import IconContainer
from .bottom import SkinCardBottom


class SkinCard(CTkFrame):
    """Главный виджет карточки скина."""
    
    def __init__(self, master, skin: Skin):
        super().__init__(master=master)
        self.__skin = skin
        self.__create_widgets()

    def __create_widgets(self):
        """Создаёт все виджеты карточки скина."""
        self.__create_icon_box()
        self.__create_skin_card_bottom()

    def __create_icon_box(self):
        """Создаёт контейнер для иконок."""
        icon_box = IconContainer(master=self, skin=self.__skin)
        icon_box.pack(side=tkinter.TOP, padx=10, pady=(10, 5))

    def __create_skin_card_bottom(self):
        """Создаёт нижнюю часть карточки."""
        skin_card_bottom = SkinCardBottom(
            master=self, 
            skin=self.__skin
        )
        skin_card_bottom.pack(fill=tkinter.BOTH, expand=True, pady=(0, 10))