from customtkinter import CTkFrame

from core.skin import Skin

class SkinCard(CTkFrame):
    def __init__(self, skin: Skin):
        self.__skin = skin

    def _get_theme_icons():
        pass