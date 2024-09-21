import os
import tkinter as tk
from tkinter import ttk
import sv_ttk
from common.get_steam_path import steam_path
from common.show_messagebox import show_messagebox

# 游戏路径常量定义
STPLUG_PATH = steam_path / 'config' / 'stplug-in'
GREENLUMA_PATH = steam_path / 'AppList'

# 分页相关常量
PAGE_SIZE = 10
current_page = 0

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
    
    # 更新页码标签
    page_label.config(text=f"Page: {current_page + 1}")

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
        show_messagebox(root, "Warning", "No game selected. Please select a game to delete.", "warning")
        return
    appid = tree.item(selected_item[0], "values")[0]
    game_type = tree.item(selected_item[0], "values")[2]
    delete_game(appid, game_type)
    show_messagebox(root, title="Success", message=f"Game: {appid}, Delete Success.", type="info")

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

# 界面设置
root = tk.Tk()
root.title("Unlocked Games Manager")
root.geometry("1024x768")

sv_ttk.use_light_theme()

search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var)
search_entry.pack(pady=10)

search_button = ttk.Button(root, text="Search", command=filter_games)
search_button.pack()

columns = ("AppID", "Name", "Type")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("AppID", text="AppID")
tree.heading("Name", text="Name")
tree.heading("Type", text="Type")
tree.pack(expand=True, fill="both")

delete_button = ttk.Button(root, text="Delete (Delete)", command=on_delete)
delete_button.pack(pady=10)

prev_button = ttk.Button(root, text="Previous Page", command=prev_page)
prev_button.pack(side=tk.LEFT, padx=10)

next_button = ttk.Button(root, text="Next Page", command=next_page)
next_button.pack(side=tk.RIGHT, padx=10)

# 添加标签来指示当前页码
page_label = ttk.Label(root, text=f"Page: {current_page + 1}")
page_label.pack(pady=10)

root.bind('<Delete>', on_key_press)
root.bind('<F5>', on_key_press)

if not (os.path.exists(STPLUG_PATH) or os.path.exists(GREENLUMA_PATH)):
    show_messagebox(root, "Error", "Both SteamTools and GreenLuma paths do not exist.", "error")
    root.destroy()
else:
    unlocked_games = load_unlocked_games()
    display_games(current_page)

root.mainloop()
