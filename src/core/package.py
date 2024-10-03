# KiryxaTech 2024, MIT License

from ooj import JsonFile
from PIL.Image import Image

from core.loader import Loader


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
        package_data = packages_data.get(package_name)

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

        default_package_name = cls.packages_file.get_entry("default_package")
        return cls.get_package(default_package_name)