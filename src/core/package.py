# KiryxaTech 2024, MIT License

from ooj import JsonFile
from PIL.Image import Image

from core.loader import Loader


class IconPackage:
    def __init__(self, name: str, images: list[Image]):
        self.name = name
        self.images = images


class IconPackageManager:
    PACKAGES_FILE_PATH = "config/packages.json"
    packages_file = JsonFile(PACKAGES_FILE_PATH)
    packages_file.create_if_not_exists()

    @classmethod
    def create_package(cls, package: IconPackage) -> None:
        packaged_array = []
        for image in package.images:
            packaged_array.append(Loader.dump_image(image))

        cls.packages_file.set_entry(package.name, packaged_array)

    @classmethod
    def get_package(cls, package_name: str) -> IconPackage:
        packages_data = cls.packages_file.read()
        package_data = packages_data.get(package_name)

        images = []
        for image_str in package_data:
            images.append(Loader.load_image(image_str))

        package = IconPackage(package_name, images)
        return package
    
    @classmethod
    def set_default_package(cls, package_name: str) -> None:
        cls.packages_file.set_entry("default_package", package_name)

    @classmethod
    def get_default_package(cls) -> IconPackage:
        cls.packages_file.update_buffer_from_file()
        
        default_package_name = cls.packages_file.get_entry("default_package")
        return cls.get_package(default_package_name)