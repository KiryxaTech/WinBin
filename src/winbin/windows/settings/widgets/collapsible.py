# Copyright (c) KiryxaTech
# This code is licensed under the MIT License.

import tkinter as tk
import customtkinter as ctk
from core.image_loader import ImageLoader, ThemedPack


class CollapsedWidget(ctk.CTkFrame):
    """
    A collapsible widget that can display an icon and title. 
    Clicking on it will expand or collapse the widget.
    
    Args:
        master (tk.Widget): The parent widget.
        iconpack (ThemedPack): The icon set to be used in the widget.
        title (str): The title to display on the widget.
        description (str, optional): A description for the widget, defaults to an empty string.
        on_click (function, optional): A function to call when the widget is clicked.
    
    Methods:
        __init__: Initializes the widget.
        _on_click: Handles the click event, triggering the on_click function.
    """
    def __init__(
        self,
        master,
        iconpack: ThemedPack,
        title: str,
        description: str = "",
        on_click=None  # Adds a parameter for passing a function to be executed on click
    ) -> None:
        """Initializes the CollapsedWidget with given parameters."""
        super().__init__(
            master=master,
            height=60,
            fg_color="transparent"
        )

        self.description = description
        self.iconpack = iconpack
        self.title = title
        self.on_click = on_click  # Store the function for later execution

        icon_label = ctk.CTkLabel(
            master=self,
            width=40,
            height=40,
            text=None,
            image=ctk.CTkImage(self.iconpack.light, self.iconpack.dark, (25, 25))
        )
        icon_label.pack(side=tk.LEFT, padx=(10, 0))

        text_frame = ctk.CTkFrame(
            master=self,
            height=40,
            fg_color="transparent"
        )
        text_frame.pack(side=tk.LEFT, padx=(15, 0), fill="both")

        title_label = ctk.CTkLabel(
            master=text_frame,
            text=self.title,
            font=("Gotham", 16)
        )
        title_label.pack(side=tk.LEFT)

        self.chevron_label = ctk.CTkLabel(  # Now it's self.chevron_label for icon manipulation
            master=self,
            width=40,
            height=40,
            text=None,
            image=ImageLoader.get_ctk_image("regular.chevronUp", 18)
        )
        self.chevron_label.pack(side=tk.RIGHT, padx=(0, 15))

        # Bind the click handler to various components
        self.bind("<Button-1>", self._on_click)
        icon_label.bind("<Button-1>", self._on_click)
        text_frame.bind("<Button-1>", self._on_click)
        title_label.bind("<Button-1>", self._on_click)
        self.chevron_label.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        """
        Handles the click event and calls the on_click function if provided.
        
        Args:
            event (tk.Event): The event object containing event details.
        
        Returns:
            None
        """
        if self.on_click:
            self.on_click()


class ExpandedWidget(ctk.CTkFrame):
    """
    A widget that can expand to display additional content.

    Args:
        master (tk.Widget): The parent widget.

    Methods:
        __init__: Initializes the ExpandedWidget.
        bind_inner_frame: Binds an inner frame to the expanded widget.
        show: Displays the content of the expanded widget.
        hide: Hides the content of the expanded widget.
    """
    def __init__(self, master):
        """Initializes the ExpandedWidget."""
        super().__init__(
            master=master,
            fg_color=("#f2f2f2", "#333333"),
            corner_radius=6
        )
        self.inner_frame = None

    def bind_inner_frame(self, frame):
        """
        Binds an inner frame to the expanded widget.

        Args:
            frame (ctk.CTkFrame): The frame to be bound to the widget.

        Returns:
            None
        """
        self.inner_frame = frame
        frame.pack(in_=self, side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def show(self):
        """
        Displays the content of the expanded widget if an inner frame is bound.

        Returns:
            None
        """
        if self.inner_frame:
            self.inner_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def hide(self):
        """
        Hides the content of the expanded widget.

        Returns:
            None
        """
        if self.inner_frame:
            self.inner_frame.pack_forget()


class CollapsibleWidget(ctk.CTkFrame):
    """
    A collapsible widget that can expand or collapse when clicked, showing or hiding additional content.

    Args:
        master (tk.Widget): The parent widget.
        iconpack (ThemedPack): The icon set to be used in the widget.
        title (str): The title of the collapsible widget.
        description (str, optional): A description of the widget, defaults to an empty string.

    Methods:
        __init__: Initializes the CollapsibleWidget.
        bind_inner_frame: Binds an inner frame to the expanded widget.
        switch_state: Switches between collapsed and expanded states.
        expand_widget: Expands the widget to show additional content.
        collapse_widget: Collapses the widget to hide additional content.
    """
    def __init__(
        self,
        master,
        iconpack: ThemedPack,
        title: str,
        description: str = ""
    ) -> None:
        """Initializes the CollapsibleWidget with given parameters."""
        super().__init__(
            master=master,
            fg_color=("#eaeaea", "#2d2d2d"),
            corner_radius=6,
            border_width=1,
            border_color=("#e5e5e5", "#1d1d1d")
        )
        self.description = description
        self.iconpack = iconpack
        self.title = title
        self._is_expanded = False

        # Collapsed widget setup
        self.__collapsed_widget = CollapsedWidget(
            master=self,
            iconpack=self.iconpack,
            title=self.title,
            description=self.description,
            on_click=self.switch_state
        )
        self.__collapsed_widget.pack(side=tk.TOP, fill=tk.BOTH, pady=6, padx=1)

        # Create expanded widget
        self.__expanded_widget = ExpandedWidget(master=self)

        self.sepparate_line = ctk.CTkFrame(
            master=self,
            fg_color=("#F3F3F3", "#202020"),
            height=2
        )

    def bind_inner_frame(self, frame):
        """
        Binds an inner frame to the expanded widget.

        Args:
            frame (ctk.CTkFrame): The frame to be bound to the widget.

        Returns:
            None
        """
        self.__expanded_widget.bind_inner_frame(frame)

    def switch_state(self):
        """
        Switches the widget between expanded and collapsed states.

        Returns:
            None
        """
        self._is_expanded = not self._is_expanded
        if self._is_expanded:
            self.expand_widget()
            self.__collapsed_widget.chevron_label.configure(
                image=ImageLoader.get_ctk_image("regular.chevronDown", 18)
            )
        else:
            self.collapse_widget()
            self.__collapsed_widget.chevron_label.configure(
                image=ImageLoader.get_ctk_image("regular.chevronUp", 18)
            )

    def expand_widget(self) -> None:
        """
        Expands the widget to show additional content.

        Returns:
            None
        """
        self.sepparate_line.pack(side=tk.TOP, fill=tk.X)
        self.__expanded_widget.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=(2, 5), padx=5)

    def collapse_widget(self) -> None:
        """
        Collapses the widget to hide additional content.

        Returns:
            None
        """
        self.sepparate_line.pack_forget()
        self.__expanded_widget.pack_forget()