import os
import tkinter as tk
from tkinter import ttk
import sv_ttk
from common.get_steam_path import steam_path
from common.show_messagebox import show_messagebox
# 游戏路径常量定义
STPLUG_PATH = steam_path / 'config' / 'stplug-in'
GREENLUMA_PATH = steam_path / 'AppList'

# 固定每页显示的游戏数量
PAGE_SIZE = 15  # 设置为固定值
current_page = 0

# 语言变量
LANGUAGE = {
    'en': {
        'title': "Unlocked Games Manager",
        'search': "Search",
        'delete': "Delete (Delete)",
        'prev_page': "Previous Page",
        'next_page': "Next Page",
        'warning': "Warning",
        'no_selection': "No game selected. Please select a game to delete.",
        'success': "Game: {}, Delete Success.",
        'error': "Error",
        'paths_not_exist': "Both SteamTools and GreenLuma paths do not exist.",
        'language_switch': "Switch Language",
        'appid': "AppID",
        'name': "Name",
        'type': "Type"
    },
    'zh': {
        'title': "解锁游戏管理器",
        'search': "搜索",
        'delete': "删除（Delete）",
        'prev_page': "上一页",
        'next_page': "下一页",
        'warning': "警告",
        'no_selection': "未选择游戏。请选择要删除的游戏。",
        'success': "游戏: {}, 删除成功。",
        'error': "错误",
        'paths_not_exist': "SteamTools 和 GreenLuma 路径都不存在。",
        'language_switch': "切换语言",
        'appid': "应用ID",
        'name': "名称",
        'type': "类型"
    }
}

current_lang = 'zh'  # 默认语言

# 界面设置
root = tk.Tk()
root.title(LANGUAGE[current_lang]['title'])
root.geometry("800x600")

search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var)
search_entry.pack(pady=10)

search_button = ttk.Button(root, text=LANGUAGE[current_lang]['search'], command=lambda: filter_games())
search_button.pack()

columns = ("AppID", "Name", "Type")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("AppID", text=LANGUAGE[current_lang]['appid'])
tree.heading("Name", text=LANGUAGE[current_lang]['name'])
tree.heading("Type", text=LANGUAGE[current_lang]['type'])
tree.pack(expand=True, fill="both")

delete_button = ttk.Button(root, text=LANGUAGE[current_lang]['delete'], command=lambda: on_delete())
delete_button.pack(pady=10)

prev_button = ttk.Button(root, text=LANGUAGE[current_lang]['prev_page'], command=lambda: prev_page())
prev_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(root, text=LANGUAGE[current_lang]['next_page'], command=lambda: next_page())
next_button.pack(side=tk.RIGHT, padx=10)

# 添加语言切换按钮
language_button = ttk.Button(root, text=LANGUAGE[current_lang]['language_switch'], command=lambda: switch_language())
language_button.pack(pady=10)

# 添加标签来指示当前页码
page_label = ttk.Label(root, text=f"{current_page + 1}/1")  # 初始化为当前页/总页数
page_label.pack(pady=10)

def load_games_from_directory(directory, extension, game_type):
    games = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(extension):
                appid = filename.replace(extension, '')
                games.append({"appid": appid, "name": f"Game {appid}", "type": game_type})
    else:
        print(f"Path not found: {directory}")
    return games

def load_unlocked_games():
    games = load_games_from_directory(STPLUG_PATH, '.st', 'SteamTools')
    games += load_games_from_directory(GREENLUMA_PATH, '.txt', 'GreenLuma')
    return games

def display_games(page):
    global page_label
    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    for row in tree.get_children():
        tree.delete(row)

    for game in unlocked_games[start_index:end_index]:
        tree.insert("", "end", values=(game["appid"], game["name"], game["type"]))

    # 计算总页数
    total_pages = (len(unlocked_games) + PAGE_SIZE - 1) // PAGE_SIZE  # 计算总页数
    # 更新页码标签
    page_label.config(text=f"{current_page + 1}/{total_pages}")

def filter_games():
    global current_page
    search_term = search_var.get().lower()
    filtered_games = [game for game in unlocked_games if any(search_term in game[field].lower() for field in ["appid", "name", "type"])]
    display_filtered_games(filtered_games)

def display_filtered_games(filtered_games):
    global current_page
    if filtered_games:
        current_page = 0
        global unlocked_games
        unlocked_games = filtered_games
        display_games(current_page)
    else:
        for row in tree.get_children():
            tree.delete(row)

def delete_game(appid, game_type):
    file_path = os.path.join(STPLUG_PATH if game_type == "SteamTools" else GREENLUMA_PATH, f"{appid}{'.st' if game_type == 'SteamTools' else '.txt'}")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
    refresh_games()

def refresh_games():
    global unlocked_games
    unlocked_games = load_unlocked_games()
    display_games(current_page)

def on_delete():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning(root, LANGUAGE[current_lang]['warning'], LANGUAGE[current_lang]['no_selection'], "warning")
        return
    appid = tree.item(selected_item[0], "values")[0]
    game_type = tree.item(selected_item[0], "values")[2]
    delete_game(appid, game_type)
    show_messagebox(root, title="Success", message=LANGUAGE[current_lang]['success'].format(appid), type="info")

def on_key_press(event):
    if event.keysym == 'Delete':
        on_delete()
    elif event.keysym == 'F5':
        refresh_games()

def next_page():
    global current_page
    if (current_page + 1) * PAGE_SIZE < len(unlocked_games):
        current_page += 1
        display_games(current_page)

def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        display_games(current_page)

def switch_language():
    global current_lang
    current_lang = 'zh' if current_lang == 'en' else 'en'
    
    # 更新窗口标题
    root.title(LANGUAGE[current_lang]['title'])
    search_button.config(text=LANGUAGE[current_lang]['search'])
    delete_button.config(text=LANGUAGE[current_lang]['delete'])
    prev_button.config(text=LANGUAGE[current_lang]['prev_page'])
    next_button.config(text=LANGUAGE[current_lang]['next_page'])
    language_button.config(text=LANGUAGE[current_lang]['language_switch'])
    
    # 更新表头
    tree.heading("AppID", text=LANGUAGE[current_lang]['appid'])
    tree.heading("Name", text=LANGUAGE[current_lang]['name'])
    tree.heading("Type", text=LANGUAGE[current_lang]['type'])

    # 更新页面标签
    total_pages = (len(unlocked_games) + PAGE_SIZE - 1) // PAGE_SIZE  # 计算总页数
    page_label.config(text=f"{current_page + 1}/{total_pages}")

if not (os.path.exists(STPLUG_PATH) or os.path.exists(GREENLUMA_PATH)):
    messagebox.showerror(LANGUAGE[current_lang]['error'], LANGUAGE[current_lang]['paths_not_exist'])
    root.destroy()
else:
    unlocked_games = load_unlocked_games()
    display_games(current_page)

root.bind('<Delete>', on_key_press)
root.bind('<F5>', on_key_press)

sv_ttk.set_theme("dark")
root.mainloop()
