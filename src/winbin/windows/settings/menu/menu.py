# KiryxaTech 2024, MIT License

import tkinter as tk
from typing import List, Optional

import customtkinter as ctk
from PIL.Image import Image

from winbin.windows.settings.utils import ACCENT_COLOR

from ..pages import Page


class MenuButton(ctk.CTkFrame):
    """Represents a clickable menu button with an icon, title, and active state."""

    buttons: List['MenuButton'] = []
    active_button: 'MenuButton' = None

    def __init__(
        self,
        master,
        icon: Image,
        active: bool = False,
        bind_page: Page | None = None
    ) -> None:
        self.is_active = active
        self.bind_page = bind_page

        super().__init__(
            master=master,
            height=35,
            corner_radius=5,
            fg_color="transparent"
        )

        self.active_line = ctk.CTkFrame(
            master=self,
            width=4,
            height=17,
            fg_color="transparent",
            corner_radius=4
        )
        self.active_line.pack(side=tk.LEFT, pady=10)

        self.image_frame = ctk.CTkLabel(
            master=self,
            image=ctk.CTkImage(icon, size=(20, 20)),
            text=None
        )
        self.image_frame.pack(side=tk.LEFT, padx=(7, 0))

        self.title = ctk.CTkLabel(
            master=self,
            text=self.bind_page.name,
            font=("Gotham", 14),
            anchor=tk.W
        )
        self.title.pack(side=tk.LEFT, padx=(10, 0))

        self.buttons.append(self)

        if self.is_active:
            self.to_active()
        
        self.bind_events()

    def bind_events(self):
        """Bind necessary events to the button."""
        self.bind_children(self, "<Button-1>", self.to_active)
        self.bind_children(self, "<Enter>", self.to_hover)
        self.bind_children(self, "<Leave>", self.to_leave)

    def to_active(self, event=None):
        """Set the button to active state."""
        if MenuButton.active_button and MenuButton.active_button != self:
            MenuButton.active_button.to_normal()

        MenuButton.active_button = self
        self.is_active = True
        self.configure(fg_color=("#eaeaea", "#2d2d2d"))
        self.active_line.configure(fg_color=ACCENT_COLOR)
        self.bind_page.show()

    def to_normal(self):
        """Set the button to normal state."""
        self.is_active = False
        self.configure(fg_color="transparent")
        self.active_line.configure(fg_color="transparent")
        self.bind_page.hide()

    def to_hover(self, event=None):
        """Handles mouse hover event."""
        hover_color = ("#ededed", "#292929") if self.is_active else ("#eaeaea", "#2d2d2d")
        self.configure(fg_color=hover_color)

    def to_leave(self, event=None):
        """Handles mouse leave event."""
        leave_color = ("#eaeaea", "#2d2d2d") if self.is_active else "transparent"
        self.configure(fg_color=leave_color)

    @staticmethod
    def bind_children(widget, event, handler):
        """Recursively bind events to widget and its children."""
        widget.bind(event, handler)
        for child in widget.winfo_children():
            MenuButton.bind_children(child, event, handler)

    def destroy(self):
        MenuButton.buttons.clear()
        MenuButton.active_button = None

        super().destroy()


class Menu(ctk.CTkScrollableFrame):
    """Scrollable menu that holds and displays multiple menu elements."""
    
    def __init__(self, master):
        super().__init__(
            master=master,
            fg_color="transparent",
            width=200,
            height=100,
            scrollbar_button_color=("#F3F3F3", "#202020"),
            scrollbar_button_hover_color=("#eaeaea", "#2d2d2d")
        )

    def pack_buttons(self):
        """Packs all the elements in reverse order."""
        for button in reversed(MenuButton.buttons):
            button.pack(side=tk.BOTTOM, fill='x', pady=(0, 3))