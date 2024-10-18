import tkinter
import customtkinter as ctk

from core.recycle_bin import RecycleBin
from core.recycle_bin.size_controller import SizeController
from core.size_converter import Size, SizeConverter
from winbin.windows.settings.utils import ACCENT_COLOR


class BinTitleWidget(ctk.CTkLabel):
    def __init__(self, master):
        recycle_bin = RecycleBin()
        max_size = SizeConverter.convert_to_max_unit(Size(recycle_bin.max_size))

        super().__init__(
            master=master,
            height=30,
            text=f"Recycle Bin (C:) – Max {max_size}",
            font=("Gotham", 18, "bold"),
            fg_color="transparent",
            anchor=tkinter.W
        )


class BinFullnessBar(ctk.CTkProgressBar):
    def __init__(self, master) -> None:
        super().__init__(
            master=master,
            height=15,
            progress_color=ACCENT_COLOR,
            orientation="horizontal",  # Устанавливаем горизонтальную ориентацию
            mode="determinate"  # Устанавливаем режим для отображения определённого прогресса
        )

        # Инициализация значения прогресса
        self.update_progress()

        # Привязываем событие изменения размера
        self.bind("<Configure>", self.update_progress)
        self.size_controller = SizeController(self.update_progress)
        self.size_controller.start_tracking()

    def update_progress(self, event=None) -> None:
        recycle_bin = RecycleBin()
        fullness_percentage = recycle_bin.total_size / recycle_bin.max_size

        # Обновляем значение прогресса в зависимости от процента заполненности
        self.set(fullness_percentage)

    def destroy(self):
        self.size_controller.stop_tracking()
        self.unbind("<Configure>")
        print(self.size_controller)
        super().destroy()


class FullnessWidgetBottom(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(
            master=master,
            height=15,
            fg_color="transparent"
        )

        recycle_bin = RecycleBin()
        total_size = recycle_bin.total_size
        max_size = recycle_bin.max_size

        used_size = SizeConverter.convert_to_max_unit(Size(total_size))
        free_size = SizeConverter.convert_to_max_unit(Size(max_size - total_size))

        font = ("Gotham", 13, "bold")

        self.used_size_field = ctk.CTkLabel(
            master=self,
            text=f"{used_size} is used",
            font=font,
            anchor=tkinter.W
        )
        self.used_size_field.pack(side=tkinter.LEFT)

        self.free_size_field = ctk.CTkLabel(
            master=self,
            text=f"{free_size} free",
            font=font,
            anchor=tkinter.E
        )
        self.free_size_field.pack(side=tkinter.RIGHT)

class BinFullnessWidget(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(
            master=master,
            height=50,
            fg_color="transparent"
        )

        self.title = BinTitleWidget(self)
        self.title.pack(side=tkinter.TOP, fill=tkinter.X)

        self.bar = BinFullnessBar(self)
        self.bar.pack(side=tkinter.TOP, fill=tkinter.X)

        self.bottom = FullnessWidgetBottom(self)
        self.bottom.pack(side=tkinter.TOP, pady=(5, 0), fill=tkinter.X)