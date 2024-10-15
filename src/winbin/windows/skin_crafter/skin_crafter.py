import customtkinter as ctk

from core.skin import SkinManager
from .skin_card import SkinCard


class SkinCrafterWindow(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#F3F3F3")
        self.title("Skin Crafter")
        self.geometry("700x400")

        self.__skin_card = SkinCard(self, SkinManager.get_default_skin())
        self.__skin_card.place(x=10, y=10)

    def show(self):
        self.mainloop()