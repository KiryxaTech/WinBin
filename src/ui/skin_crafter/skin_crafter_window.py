import customtkinter as ctk

from core.skin import SkinManager
from ui.skin_crafter.skins_page.skin_card.skin_card import SkinCardWidget


class SkinBuilderWindow(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#F3F3F3")
        self.title("Skin Crafter")
        self.geometry("700x400")

        self.__skin_card = SkinCardWidget(self, SkinManager.get_default_skin())
        self.__skin_card.place(x=10, y=10)

    def show(self):
        self.mainloop()