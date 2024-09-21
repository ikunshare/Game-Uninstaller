import os
import tkinter as tk
from tkinter import ttk
import sv_ttk
from common.get_steam_path import steam_path
from common.show_messagebox import show_messagebox

def load_unlocked_games():
    games = []

    if os.path.exists(stplug_path):
        for filename in os.listdir(stplug_path):
            if filename.endswith('.st'):
                appid = filename.replace('.st', '')
                games.append({"appid": appid, "name": f"Game {appid}", "type": "SteamTools"})
    else:
        print(f"Path not found: {stplug_path}")
    
    if os.path.exists(greenluma_path):
        for filename in os.listdir(greenluma_path):
            if filename.endswith('.txt'):
                appid = filename.replace('.txt', '')
                games.append({"appid": appid, "name": f"Game {appid}", "type": "GreenLuma"})
    else:
        print(f"Path not found: {greenluma_path}")
    
    return games

def filter_games():
    search_term = search_var.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for game in unlocked_games:
        if search_term in game["appid"].lower() or search_term in game["name"].lower() or search_term in game["type"].lower():
            tree.insert("", "end", values=(game["appid"], game["name"], game["type"]))

def delete_game(appid, game_type):
    if game_type == "SteamTools":
        file_path = os.path.join(stplug_path, f"{appid}.st")
    elif game_type == "GreenLuma":
        file_path = os.path.join(greenluma_path, f"{appid}.txt")
    
    if os.path.exists(file_path):
        os.remove(file_path)
    refresh_games()

def refresh_games():
    global unlocked_games
    unlocked_games = load_unlocked_games()
    filter_games()

def on_delete():
    selected_item = tree.selection()
    if not selected_item:
        show_messagebox(root, "Warning", "No game selected. Please select a game to delete.", "warning")
        return
    appid = tree.item(selected_item[0], "values")[0]
    game_type = tree.item(selected_item[0], "values")[2]
    delete_game(appid, game_type)
    show_messagebox(root, title="Success", message=f"Game: {appid}, Delete Success.", type="warning")

def on_key_press(event):
    if event.keysym == 'Delete':
        on_delete()
    elif event.keysym == 'F5':
        refresh_games()

root = tk.Tk()
root.title("Unlocked Games Manager")
root.geometry("600x400")

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

root.bind('<Delete>', on_key_press)
root.bind('<F5>', on_key_press)

stplug_path = steam_path / 'config' / 'stplug-in'
greenluma_path = steam_path / 'AppList' 

if not os.path.exists(stplug_path) and not os.path.exists(greenluma_path):
    show_messagebox(root, "Error", "Both SteamTools and GreenLuma paths do not exist.", "error")
    root.destroy()
else:
    unlocked_games = load_unlocked_games()
    filter_games()

root.mainloop()
