# KiryxaTech 2024, MIT License

from threading import Thread

from core.recycle_bin import RecycleBin
from core.skin import SkinManager
from winbin.tray import TrayIcon


DRIVE_LETTER = "C:"


def start_tray_icon():
    """ Starts the tray icon in a separate thread. """

    recycle_bin = RecycleBin(DRIVE_LETTER)
    bin_skin = SkinManager.get_default_skin()

    bin_tray_icon = TrayIcon(bin_skin, recycle_bin)

    bin_tray_icon.start()


def main():
    """ The main function of the program that starts all processes. """

    start_tray_icon()


if __name__ == "__main__":
    main()