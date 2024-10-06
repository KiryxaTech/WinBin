# KiryxaTech 2024, MIT License

from threading import Thread

from core.recycle_bin import RecycleBin
from core.skin import Skin, SkinManager
from bin_icon import BinIcon


def main():
    skin = SkinManager.get_default_skin()

    recycle_bin = RecycleBin("C:")
    bin = BinIcon(skin, recycle_bin)

    bin_thread = Thread(target=bin.run)
    bin_thread.start()

    bin.start_background_update()

if __name__ == "__main__":
    main()