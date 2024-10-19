# KiryxaTech 2024, MIT License

import io
import base64
from pathlib import Path

import customtkinter as ctk
import PIL.Image
from PIL.Image import Image


class ThemedPack:
    def __init__(self, light: Image, dark: Image) -> None:
        self.light = light
        self.dark = dark


class ImageLoader:
    @staticmethod
    def to_image(image_str: str) -> Image:

        image_bytes = base64.b64decode(image_str)
        image = PIL.Image.open(io.BytesIO(image_bytes))

        return image
    
    @staticmethod
    def to_bytes(image: Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_str = base64.b64encode(buffered.getvalue()).decode()

        return image_str
    
    @staticmethod
    def get_themed_pack(pack_lib: str) -> ThemedPack:
        try:
            light_image = ImageLoader.get_image(f"{pack_lib}.light")
            dark_image = ImageLoader.get_image(f"{pack_lib}.dark")
        except FileNotFoundError:
            raise ValueError(f"Image library '{pack_lib}' not found")

        return ThemedPack(light_image, dark_image)
    
    @staticmethod
    def get_ctk_image(pack_lib: str, size: int = 20) -> ctk.CTkImage:
        themed_pack = ImageLoader.get_themed_pack(pack_lib)
        return ctk.CTkImage(
            light_image=themed_pack.light,
            dark_image=themed_pack.dark,
            size=(size, size)
        )
    
    @staticmethod
    def get_image(pack_lib: str):
        image_path = Path("assets", "icons", f"{pack_lib.replace(".", r"\\")}.png")
        image = PIL.Image.open(image_path)
        return image