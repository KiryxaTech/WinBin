import json

import darkdetect
from PIL.Image import Image

from core.loader import Loader


class Skin:
    def __init__(
            self,
            name: str,
            light_icons: list[Image],
            dark_icons: list[Image]
        ) -> None:
        
        self.name = name
        self.light_icons = light_icons
        self.dark_icons = dark_icons

    def get_icons_from_theme(self) -> list[Image]:
        if darkdetect.isLight():
            return self.dark_icons
        else:
            return self.light_icons

    def to_dict(self) -> dict:
        return {
            "lightIcons": [Loader.to_bytes(img) for img in self.light_icons],
            "darkIcons": [Loader.to_bytes(img) for img in self.dark_icons]
        }

    @staticmethod
    def from_dict(name: str, data: dict) -> 'Skin':
        return Skin(
            name=name,
            light_icons=[Loader.to_image(bytes_data) for bytes_data in data["lightIcons"]],
            dark_icons=[Loader.to_image(bytes_data) for bytes_data in data["darkIcons"]]
        )


class SkinManager:
    SKINS_FILE_PATH = r"config\skins.json"

    @classmethod
    def add_skin(cls, skin: Skin) -> None:
        data = cls._load_data()
        data["skins"][skin.name] = skin.to_dict()
        cls._save_data(data)

    @classmethod
    def remove_skin(cls, skin_name: str):
        data = cls._load_data()
        if skin_name in data["skins"]:
            del data["skins"][skin_name]
            cls._save_data(data)

    @classmethod
    def get_skin(cls, skin_name: str) -> Skin:
        data = cls._load_data()
        skin_data = data["skins"].get(skin_name)
        if skin_data:
            return Skin.from_dict(skin_name, skin_data)
        raise ValueError(f"Skin with name {skin_name} not found")

    @classmethod
    def get_default_skin(cls) -> Skin:
        data = cls._load_data()
        default_skin_name = data.get("defaultSkin")
        if default_skin_name:
            return cls.get_skin(default_skin_name)
        raise ValueError("Default skin not set")

    @classmethod
    def set_default_skin(cls, skin_name: str) -> None:
        """Устанавливает стандартный скин."""
        data = cls._load_data()
        if skin_name in data["skins"]:
            data["defaultSkin"] = skin_name
            cls._save_data(data)
        else:
            raise ValueError(f"Skin {skin_name} does not exist")

    @classmethod
    def _load_data(cls) -> dict:
        """Загружает данные скинов из JSON-файла."""
        try:
            with open(cls.SKINS_FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"defaultSkin": "", "skins": {}}

    @classmethod
    def _save_data(cls, data: dict) -> None:
        """Сохраняет данные скинов в JSON-файл."""
        with open(cls.SKINS_FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)