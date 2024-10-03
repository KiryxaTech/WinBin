# KiryxaTech 2024, MIT License

from threading import Thread

import PIL.Image

from core.package import PackageManager
from bin import BinIcon


def main():
    package = PackageManager.read_package(PackageManager.get_default_package())
    icons = package.images
    icons_count = len(icons)

    bin = BinIcon(icons[0])

    bin_thread = Thread(target=bin.run)
    bin_thread.start()

    bin.update_icon(icons[icons_count - 2])

if __name__ == "__main__":
    main()