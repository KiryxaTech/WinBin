import customtkinter as ctk


class SkinBuilderWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Skin Creator")
        self.geometry("400x700")

    def show(self):
        self.mainloop()