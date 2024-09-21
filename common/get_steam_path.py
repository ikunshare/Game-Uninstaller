import winreg

from pathlib import Path

def get_steam_path():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam')
        steam_path = Path(winreg.QueryValueEx(key, 'SteamPath')[0])
        return steam_path
    
steam_path = get_steam_path()