import winreg


def get_adjusted_accent_color():
    """Извлекает акцентный цвет из реестра и применяет затемнение и осветление."""
    
    registry_path = r"Software\Microsoft\Windows\DWM"
    
    try:
        # Открываем ключ реестра
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path)
        
        # Читаем значения AccentColor
        accent_color, _ = winreg.QueryValueEx(reg_key, "AccentColor")
        winreg.CloseKey(reg_key)
        
        # Извлекаем акцентный цвет в формате RGB (BGR -> RGB)
        bgr_color = accent_color & 0xFFFFFF
        rgb_color = (bgr_color & 0xFF, (bgr_color >> 8) & 0xFF, (bgr_color >> 16) & 0xFF)

        # Фактор затемнения, который имитирует поведение Windows
        darkening_factor = 1.2
        darkened_color = tuple(c for c in rgb_color)

        # Фактор осветления
        lightening_factor = 2.2
        lightened_color = tuple(min(c, 255) for c in rgb_color)

        # Конвертируем в HEX
        darkened_hex = "#{:02x}{:02x}{:02x}".format(darkened_color[0], darkened_color[1], darkened_color[2])
        lightened_hex = "#{:02x}{:02x}{:02x}".format(lightened_color[0], lightened_color[1], lightened_color[2])

        return darkened_hex, lightened_hex
    
    except FileNotFoundError:
        print("Не удалось найти необходимые параметры в реестре.")
        return None, None

ACCENT_COLOR = get_adjusted_accent_color()