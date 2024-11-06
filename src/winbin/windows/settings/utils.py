import winaccent


class ColorUtils:
    @staticmethod
    def accent() -> tuple[str, str]:
        return (winaccent.accent_dark, winaccent.accent_light)
    
    @staticmethod
    def noactive_menu_button() -> str:
        return "transparent"
    
    @staticmethod
    def active_menu_button() -> tuple[str, str]:
        return ("#eaeaea", "#2d2d2d")