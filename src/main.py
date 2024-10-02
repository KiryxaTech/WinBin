# KiryxaTech 2024, MIT License

import PIL.Image
from loader import Loader
from bin import Bin
from package import Package, PackageManager


def main():
    images = []
    for i in range(4):
        images.append(PIL.Image.open(f"bin_{i}.png"))

    package = Package(
        name="Windows 11 Icons",
        images=images
    )
    PackageManager.write_package(package)

    print(len(PackageManager.read_package("Windows 11 Icons").images))

if __name__ == "__main__":
    main()