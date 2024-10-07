# KiryxaTech 2024, MIT License

import win32com.client
import ctypes
import winreg
import os
from typing import Optional
from ooj import JsonFile

from core.size_converter import Size, SizeConverter


class SHQUERYRBINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', ctypes.c_ulong),  # Size of the structure
        ('i64Size', ctypes.c_longlong),  # Total size of items in the recycle bin
        ('i64NumItems', ctypes.c_longlong),  # Number of items in the recycle bin
    ]


class RecycleBin:
    RECYCLE_BIN_NAMESPACE = 10
    BIN_REGISTRY_PATH = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\BitBucket"
    MAX_CAPACITY_PARAM_NAME = "MaxCapacity"
    GUID_PARAM_NAME = "LastEnum"

    def __init__(self, drive_letter: Optional[str] = "C:") -> None:
        """Initialize the RecycleBin with the specified drive letter.

        Args:
            drive_letter (Optional[str]): The drive letter for which the recycle bin should be managed. Defaults to "C:".
        """
        self.drive_letter = drive_letter

    @property
    def total_size(self) -> int:
        """Get the total size of files and folders in the recycle bin.

        Returns:
            int: Total size of items in the recycle bin in bytes.
        """
        return self._calculate_total_bin_size()

    @property
    def item_count(self) -> int:
        """Get the count of files and folders in the recycle bin.

        Returns:
            int: Number of items in the recycle bin.
        """
        return self._get_item_count()

    @property
    def max_size(self) -> int:
        """Get the maximum size of the recycle bin in bytes.

        Returns:
            int: Maximum size of the recycle bin in bytes.
        """
        return self._get_max_bin_size()

    def set_max_bin_size(self, size_in_bytes: int) -> None:
        """Set the maximum size of the recycle bin for the specified drive.

        Args:
            size_in_bytes (int): The maximum size in bytes.
        """
        size_in_mb = SizeConverter.convert(Size(size_in_bytes, Size.B), Size.MB)
        self._set_max_bin_size(size_in_mb)

    def clear_bin(self) -> None:
        """Clear the recycle bin by removing all items."""
        window_handle = None  # Window handle for confirmation dialog
        root_path = None  # Path to the root of the recycle bin

        configurate = JsonFile(r"config\configurate.json")
        configurate.update_buffer_from_file()
        ask_defore_cleaning = configurate.get_entry("ask_before_cleaning")
        if ask_defore_cleaning:
            flags = 0  # Flags for operation (e.g., confirmation of cleaning)
        else:
            flags = 1
        ctypes.windll.shell32.SHEmptyRecycleBinA(window_handle, root_path, flags)

    def open_bin_in_explorer(self) -> None:
        os.system("explorer.exe ::{645FF040-5081-101B-9F08-00AA002F954E}")

    def _calculate_total_bin_size(self) -> int:
        """Calculate the total size of files and folders in the recycle bin.

        Returns:
            int: Total size in bytes.
        """
        windows_shell = win32com.client.Dispatch("Shell.Application")
        recycle_bin = windows_shell.NameSpace(self.RECYCLE_BIN_NAMESPACE)
        total_size = 0

        def get_item_size(item):
            nonlocal total_size
            if item.IsFolder:
                try:
                    folder = windows_shell.NameSpace(item.Path)
                    for sub_item in folder.Items():
                        get_item_size(sub_item)
                except:
                    pass
            else:
                total_size += item.Size

        for item in recycle_bin.Items():
            get_item_size(item)

        return total_size

    def _get_item_count(self) -> int:
        """Get the item count using SHQueryRecycleBinW.

        Returns:
            int: Count of items in the recycle bin.
        """
        SHQueryRecycleBin = ctypes.windll.shell32.SHQueryRecycleBinW

        rb_info = SHQUERYRBINFO()
        rb_info.cbSize = ctypes.sizeof(SHQUERYRBINFO)
        recycle_bin_path = f"{self.drive_letter}\\"  # Path to the recycle bin on the specified drive

        result = SHQueryRecycleBin(recycle_bin_path, ctypes.byref(rb_info))
        if result == 0:  # If successful operation (S_OK)
            return rb_info.i64NumItems
        return 0

    def _set_max_bin_size(self, size: Size) -> bool:
        """Update the MaxCapacity value for the specified drive in the registry.

        Args:
            size (Size): The size object representing the maximum capacity.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        status = True
        try:
            bin_guid = self._get_bin_guid()
            bin_registry_key = os.path.join(self.BIN_REGISTRY_PATH, "Volume", bin_guid)

            with winreg.OpenKey(
                key=winreg.HKEY_CURRENT_USER,
                sub_key=bin_registry_key,
                access=winreg.KEY_WRITE
            ) as bin_key:
                
                # Set max capacity param in registry
                winreg.SetValueEx(
                    key=bin_key,
                    value_name=self.MAX_CAPACITY_PARAM_NAME,
                    type=winreg.REG_DWORD,
                    value=SizeConverter.convert_to_bytes(size)
                )

        except OSError:
            status = False

        return status

    def _get_bin_guid(self) -> str:
        """Get the GUID of the last volume from the registry.

        Returns:
            str: The GUID of the last volume.
        """
        with winreg.OpenKey(
            key=winreg.HKEY_CURRENT_USER,
            sub_key=self.BIN_REGISTRY_PATH
        ) as bin_key:
            
            bin_guid_list, _ = winreg.QueryValueEx(bin_key, self.GUID_PARAM_NAME)
            bin_guid = bin_guid_list[0].split(",")[1]  # Extract the GUID from the registry value

            return bin_guid

    def _get_max_bin_size(self) -> int:
        """Get the maximum size of the recycle bin from the registry.

        Returns:
            int: Maximum size of the recycle bin in bytes.
        """
        try:
            bin_guid = self._get_bin_guid()
            bin_registry_key = os.path.join(self.BIN_REGISTRY_PATH, "Volume", bin_guid)

            with winreg.OpenKey(
                key=winreg.HKEY_CURRENT_USER,
                sub_key=bin_registry_key
            ) as volume_key:
                
                max_size_in_mb, _ = winreg.QueryValueEx(volume_key, "MaxCapacity")
                max_size_in_b = SizeConverter.convert_to_bytes(Size(max_size_in_mb, Size.MB))

                return max_size_in_b
            
        except OSError:
            return 0