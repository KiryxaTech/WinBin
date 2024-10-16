import tkinter

from customtkinter import CTkButton, CTkImage
from PIL import Image


class SkinCardButton(CTkButton):
    def __init__(
        self,
        master,
        icon_name: str,
        action: callable,
        active_color: str,
        hover_color: str | None = None,
        press_color: str | None = None,
        disable_color: str | None = None,
        is_disable: bool = False
    ) -> None:
        
        icon_path = f"assets\\{icon_name}.png"

        self.icon = CTkImage(
            light_image=Image.open(icon_path),
            dark_image=Image.open(icon_path),
            size=(20, 20)
        )

        self.action = action
        self.active_color = active_color
        self.hover_color = hover_color or active_color  # если hover_color не задан, используем active_color
        self.press_color = press_color or active_color  # если press_color не задан, используем active_color
        self.disable_color = disable_color or "#D3D3D3"

        super().__init__(
            master=master,
            width=30,
            height=20,
            corner_radius=7,
            image=self.icon,
            text=None
        )

        self.disable() if is_disable else self.enable()

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def enable(self):
        """Включить кнопку."""
        self.configure(
            command=self.action,
            fg_color=self.active_color,
            state="normal"
        )

    def disable(self):
        """Отключить кнопку."""
        self.configure(
            command=None,
            fg_color=self.disable_color or self.active_color,
            state="disabled"
        )

    def right_pack(self):
        self.pack(side=tkinter.RIGHT, padx=(0, 10))

    def on_press(self, event):
        """Изменить цвет кнопки при нажатии."""
        if self.cget("state") == "normal":  # Проверяем, что кнопка не отключена
            self.configure(fg_color=self.press_color)

    def on_release(self, event):
        """Вернуть цвет кнопки после нажатия."""
        if self.cget("state") == "normal":
            self.configure(fg_color=self.active_color)

    def on_enter(self, event):
        """Изменить цвет кнопки при наведении курсора."""
        if self.cget("state") == "normal":
            self.configure(fg_color=self.hover_color)

    def on_leave(self, event):
        """Вернуть цвет кнопки при убирании курсора."""
        if self.cget("state") == "normal":
            self.configure(fg_color=self.active_color)
