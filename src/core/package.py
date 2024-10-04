# KiryxaTech 2024, MIT License

from ooj import JsonFile
from PIL.Image import Image

from core.loader import Loader


DEFAULT_PACKAGE = {
    "default_package": "Windows 11 Icons",
    "Windows 11 Icons": [
        "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"
    ]
}


class IconPackage:
    def __init__(self, name: str, images: list[Image]) -> None:
        """
        Initializes an IconPackage instance.

        Parameters:
            name (str): The name of the icon package.
            images (list[Image]): A list of images associated with the package.
        """
        self.name = name
        self.images = images


class IconPackageManager:
    PACKAGES_FILE_PATH = "config/packages.json"
    packages_file = JsonFile(PACKAGES_FILE_PATH)
    packages_file.create_if_not_exists()

    @classmethod
    def create_package(cls, package: IconPackage) -> None:
        """
        Creates a new icon package and stores it in the JSON file.

        Parameters:
            package (IconPackage): The icon package to create.
        """
        packaged_array = []
        for image in package.images:
            packaged_array.append(Loader.dump_image(image))

        cls.packages_file.set_entry(package.name, packaged_array)

    @classmethod
    def get_package(cls, package_name: str) -> IconPackage:
        """
        Retrieves an icon package by its name.

        Parameters:
            package_name (str): The name of the icon package to retrieve.

        Returns:
            IconPackage: The requested icon package containing images.
        """
        packages_data = cls.packages_file.read()
        try:
            package_data = packages_data.get(package_name)
        except KeyError:
            package_data = DEFAULT_PACKAGE

        images = []
        for image_str in package_data:
            images.append(Loader.load_image(image_str))

        package = IconPackage(package_name, images)
        return package

    @classmethod
    def set_default_package(cls, package_name: str) -> None:
        """
        Sets the default icon package by name.

        Parameters:
            package_name (str): The name of the icon package to set as default.
        """
        cls.packages_file.set_entry("default_package", package_name)

    @classmethod
    def get_default_package(cls) -> IconPackage:
        """
        Retrieves the currently set default icon package.

        Returns:
            IconPackage: The default icon package containing images.
        """
        cls.packages_file.update_buffer_from_file()

        try:
            default_package_name = cls.packages_file.get_entry("default_package")
        except KeyError:
            images = []
            for image_str in DEFAULT_PACKAGE["Windows 11 Icons"]:
                images.append(Loader.load_image(image_str))
            return IconPackage(DEFAULT_PACKAGE["default_package"], images)
        
        return cls.get_package(default_package_name)