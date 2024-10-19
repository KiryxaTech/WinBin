# KiryxaTech 2024, MIT License

import tkinter
import customtkinter as ctk

class Page(ctk.CTkFrame):
    def __init__(self, master, name: str):
        super().__init__(
            master=master,
            fg_color="transparent"
        )

        self.name = name

        self.title = ctk.CTkLabel(
            master=self,
            text=self.name,
            font=("Gotham", 22, "bold")
        )
        self.title.pack(side='top', anchor=tkinter.W)

    def show(self):
        self.pack(side="right", padx=25, pady=15, fill='both', expand=True)

    def hide(self):
        self.pack_forget()