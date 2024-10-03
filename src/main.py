# KiryxaTech 2024, MIT License

from threading import Thread

from core import PackageManager, RecycleBin
from bin_icon import BinIcon


def main():
    package = PackageManager.read_package(PackageManager.get_default_package())

    recycle_bin = RecycleBin("C:")
    bin = BinIcon(package, recycle_bin)

    bin_thread = Thread(target=bin.run)
    bin_thread.start()

    bin.start_background_update()

if __name__ == "__main__":
    main()