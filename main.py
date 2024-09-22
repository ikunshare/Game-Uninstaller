import os
import tkinter as tk
from tkinter import ttk
import sv_ttk
from common.get_steam_path import steam_path  # 自定义模块，获取Steam路径
from common.show_messagebox import show_messagebox  # 自定义模块，用于显示消息框
from common.i18n import LANGUAGE  # 自定义模块，多语言支持

# 定义路径
STPLUG_PATH = steam_path / 'config' / 'stplug-in'
GREENLUMA_PATH = steam_path / 'AppList'

# 每页显示的游戏数量
PAGE_SIZE = 14

# 当前页码和语言
current_page = 0
current_lang = 'zh'

# 初始化主窗口
root = tk.Tk()
root.title(LANGUAGE[current_lang]['title'])
root.geometry("800x600")

# 搜索框
search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var)
search_entry.pack(pady=10)

# 搜索按钮
search_button = ttk.Button(root, text=LANGUAGE[current_lang]['search'], command=lambda: filter_games())
search_button.pack()

# 定义表格的列
columns = ("AppID", "Name", "Type")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("AppID", text=LANGUAGE[current_lang]['appid'])
tree.heading("Name", text=LANGUAGE[current_lang]['name'])
tree.heading("Type", text=LANGUAGE[current_lang]['type'])
tree.pack(expand=True, fill="both")

# 删除按钮
delete_button = ttk.Button(root, text=LANGUAGE[current_lang]['delete'], command=lambda: on_delete())
delete_button.pack(pady=10)

# 翻页按钮
prev_button = ttk.Button(root, text=LANGUAGE[current_lang]['prev_page'], command=lambda: prev_page())
prev_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(root, text=LANGUAGE[current_lang]['next_page'], command=lambda: next_page())
next_button.pack(side=tk.RIGHT, padx=10)

# 语言切换按钮
language_button = ttk.Button(root, text=LANGUAGE[current_lang]['language_switch'], command=lambda: switch_language())
language_button.pack(pady=10)

# 页码标签
page_label = ttk.Label(root, text=f"{current_page + 1}/1")
page_label.pack(pady=10)

def steamtools_load(directory, extension, game_type):
    """
    加载SteamTools的游戏信息
    """
    games = []
    if os.path.exists(directory):
        try:
            for filename in os.listdir(directory):
                if filename.endswith(extension):
                    appid = filename.replace(extension, '')
                    games.append({
                        "appid": appid,
                        "name": f"Game {appid}",
                        "type": game_type,
                        "filename": filename  # 记录文件名
                    })
        except Exception as e:
            print(f"Error accessing directory {directory}: {e}")
    else:
        print(f"Path not found: {directory}")
    return games

def greenluma_load(directory, extension, game_type):
    """
    加载GreenLuma的游戏信息
    """
    games = []
    if os.path.exists(directory):
        try:
            for filename in os.listdir(directory):
                if filename.endswith(extension):
                    try:
                        file_path = os.path.join(directory, filename)
                        with open(file_path, encoding='utf8') as f:
                            appid = f.read().strip()
                        games.append({
                            "appid": appid,
                            "name": f"Game {appid}",
                            "type": game_type,
                            "filename": filename  # 记录文件名
                        })
                    except Exception as e:
                        print(f"Error reading file {filename}: {e}")
        except Exception as e:
            print(f"Error accessing directory {directory}: {e}")
    else:
        print(f"Path not found: {directory}")
    return games

def load_unlocked_games():
    """
    加载所有解锁的游戏
    """
    games = steamtools_load(STPLUG_PATH, '.st', 'SteamTools')
    games += greenluma_load(GREENLUMA_PATH, '.txt', 'GreenLuma')
    return games

def display_games(page):
    """
    显示指定页码的游戏
    """
    global page_label
    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    # 清空当前的表格数据
    for row in tree.get_children():
        tree.delete(row)

    # 显示新页的数据
    for game in unlocked_games[start_index:end_index]:
        tree.insert("", "end", values=(game["appid"], game["name"], game["type"]))

    # 更新页数标签
    total_pages = (len(unlocked_games) + PAGE_SIZE - 1) // PAGE_SIZE
    page_label.config(text=f"{current_page + 1}/{total_pages}")

def filter_games():
    """
    根据搜索词过滤游戏
    """
    global current_page, unlocked_games
    search_term = search_var.get().lower()
    filtered_games = [
        game for game in unlocked_games
        if any(search_term in game[field].lower() for field in ["appid", "name", "type"])
    ]
    display_filtered_games(filtered_games)

def display_filtered_games(filtered_games):
    """
    显示过滤后的游戏列表
    """
    global current_page, unlocked_games
    if filtered_games:
        current_page = 0
        unlocked_games = filtered_games
        display_games(current_page)
    else:
        # 如果没有匹配的结果，清空表格
        for row in tree.get_children():
            tree.delete(row)
        page_label.config(text="0/0")

def delete_game(appid, game_type):
    """
    删除指定的游戏文件
    """
    # 查找对应的游戏条目
    game_to_delete = None
    for game in unlocked_games:
        if game["appid"] == appid and game["type"] == game_type:
            game_to_delete = game
            break

    if not game_to_delete:
        print(f"Game with AppID {appid} and type {game_type} not found.")
        return

    try:
        if game_type == "SteamTools":
            file_path = os.path.join(STPLUG_PATH, game_to_delete["filename"])
        elif game_type == "GreenLuma":
            file_path = os.path.join(GREENLUMA_PATH, game_to_delete["filename"])
        else:
            print(f"Unknown game type: {game_type}")
            return

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File does not exist: {file_path}")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

    refresh_games()

def refresh_games():
    """
    刷新游戏列表
    """
    global unlocked_games, current_page
    unlocked_games = load_unlocked_games()
    display_games(current_page)

def on_delete():
    """
    处理删除按钮点击事件
    """
    selected_item = tree.selection()
    if not selected_item:
        show_messagebox(root, LANGUAGE[current_lang]['warning'], LANGUAGE[current_lang]['no_selection'], "warning")
        return
    appid = tree.item(selected_item[0], "values")[0]
    game_type = tree.item(selected_item[0], "values")[2]
    delete_game(appid, game_type)
    show_messagebox(root, title=LANGUAGE[current_lang]['success_title'], message=LANGUAGE[current_lang]['success'].format(appid), type="info")

def on_key_press(event):
    """
    处理键盘按键事件
    """
    if event.keysym == 'Delete':
        on_delete()
    elif event.keysym == 'F5':
        refresh_games()

def next_page():
    """
    显示下一页游戏
    """
    global current_page
    if (current_page + 1) * PAGE_SIZE < len(unlocked_games):
        current_page += 1
        display_games(current_page)

def prev_page():
    """
    显示上一页游戏
    """
    global current_page
    if current_page > 0:
        current_page -= 1
        display_games(current_page)

def switch_language():
    """
    切换语言
    """
    global current_lang
    current_lang = 'zh' if current_lang == 'en' else 'en'
    
    root.title(LANGUAGE[current_lang]['title'])
    search_button.config(text=LANGUAGE[current_lang]['search'])
    delete_button.config(text=LANGUAGE[current_lang]['delete'])
    prev_button.config(text=LANGUAGE[current_lang]['prev_page'])
    next_button.config(text=LANGUAGE[current_lang]['next_page'])
    language_button.config(text=LANGUAGE[current_lang]['language_switch'])
    
    tree.heading("AppID", text=LANGUAGE[current_lang]['appid'])
    tree.heading("Name", text=LANGUAGE[current_lang]['name'])
    tree.heading("Type", text=LANGUAGE[current_lang]['type'])

    # 更新页数标签
    total_pages = (len(unlocked_games) + PAGE_SIZE - 1) // PAGE_SIZE
    page_label.config(text=f"{current_page + 1}/{total_pages}")

# 检查路径是否存在，如果不存在则显示错误消息并关闭程序
if not (os.path.exists(STPLUG_PATH) or os.path.exists(GREENLUMA_PATH)):
    show_messagebox(root, LANGUAGE[current_lang]['error'], LANGUAGE[current_lang]['paths_not_exist'], "error")
    root.destroy()
else:
    # 加载并显示游戏列表
    unlocked_games = load_unlocked_games()
    display_games(current_page)

# 绑定键盘事件
root.bind('<Delete>', on_key_press)
root.bind('<F5>', on_key_press)

# 设置主题
sv_ttk.set_theme("light")

# 运行主循环
root.mainloop()
