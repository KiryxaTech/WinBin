# KiryxaTech 2024, MIT License

import customtkinter as ctk
import PIL.Image

from core.image_loader import ImageLoader

from .pages import Page, HomePage
from .menu import Menu, MenuButton


# TODO: Fix to the bug created more instances error.
class SettingsWindow(ctk.CTk):
    instance: 'SettingsWindow' = None

    def __init__(self, *args, **kwargs):
        super().__init__(fg_color=("#F3F3F3", "#202020"))

        self.title("Winbin - Settings")
        self.geometry("1000x600")
        # self.minsize(600, 400)
        self.attributes('-alpha', 0.994)

        self.menu = Menu(self)

        self.tab_button_index = 0

        home_page = HomePage(self)
        MenuButton(
            master=self.menu,
            icon=ImageLoader.get_image("menu.home"),
            active=True,
            bind_page=home_page,
        )

        skins_page = Page(self, "Skins")
        MenuButton(
            master=self.menu,
            icon=ImageLoader.get_image("menu.skins"),
            bind_page=skins_page
        )

        settings_page = Page(self, "Settings")
        MenuButton(
            master=self.menu,
            icon=ImageLoader.get_image("menu.settings"),
            bind_page=settings_page
        )

        about_page = Page(self, "About")
        MenuButton(
            master=self.menu,
            icon=ImageLoader.get_image("menu.about"),
            bind_page=about_page
        )
        
        self.menu.pack(side='left', padx=15, pady=15, fill='y')
        self.menu.pack_buttons()

    def destroy(self):
        super().destroy()