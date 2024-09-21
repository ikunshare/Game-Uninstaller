import winreg
from pathlib import Path

def get_steam_path():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Valve\Steam') as key:
            steam_path = Path(winreg.QueryValueEx(key, 'SteamPath')[0])
            return steam_path
    except FileNotFoundError:
        print("未找到 Steam 安装路径，请确保 Steam 已安装。")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

steam_path = get_steam_path()

