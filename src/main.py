# KiryxaTech 2024, MIT License

from threading import Thread

from core.recycle_bin import RecycleBin
from core.skin import SkinManager
from winbin.tray import TrayIcon


def main():
    skin = SkinManager.get_default_skin()

    recycle_bin = RecycleBin("C:")
    bin = TrayIcon(skin, recycle_bin)

    bin_thread = Thread(target=bin.run)
    bin_thread.start()


if __name__ == "__main__":
    main()