import tkinter
from PIL import Image
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkImage
from core.skin import Skin, SkinManager
from ui.skin_crafter.skins_page.skin_card.icon_box import IconBoxWidget


class SkinCardActionButton(CTkButton):
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

        # Изначально задаем состояние кнопки
        if is_disable:
            self.disable()
        else:
            self.enable()

        # Привязываем события для нажатия и отпускания кнопки
        self.bind("<ButtonPress-1>", self.on_press)  # при нажатии левой кнопки мыши
        self.bind("<ButtonRelease-1>", self.on_release)  # при отпускании левой кнопки мыши
        self.bind("<Enter>", self.on_enter)  # при наведении курсора на кнопку
        self.bind("<Leave>", self.on_leave)  # при убирании курсора с кнопки

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


class SkinCardBottomWidget(CTkFrame):
    """Виджет для нижней части карточки скина."""
    
    def __init__(self, master, skin: Skin, apply_callback):
        super().__init__(master=master, height=30, fg_color="transparent")
        self.__skin = skin
        self.__apply_callback = apply_callback
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
        self.apply_button = SkinCardActionButton(
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

        self.delete_button = SkinCardActionButton(
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
        self.__apply_callback(self.__skin)

    def __delete_skin(self):
        SkinManager.remove_skin(self.__skin.name)
        print("Скин удалён!")
        self.master.destroy()


class SkinCardWidget(CTkFrame):
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
        icon_box = IconBoxWidget(master=self, skin=self.__skin)
        icon_box.pack(side=tkinter.TOP, padx=10, pady=(10, 5))

    def __create_skin_card_bottom(self):
        """Создаёт нижнюю часть карточки."""
        skin_card_bottom = SkinCardBottomWidget(
            master=self, 
            skin=self.__skin, 
            apply_callback=self.__apply_skin
        )
        skin_card_bottom.pack(fill=tkinter.BOTH, expand=True, pady=(0, 10))

    def __apply_skin(self, skin: Skin):
        """Применяет выбранный скин через SkinManager."""
        SkinManager.set_default_skin(skin.name)