from tkinter import messagebox
import tkinter as tk

def show_messagebox(parent, title, message, type="info"):
    """
    显示消息框并确保其在顶部显示
    :param parent: 父窗口
    :param title: 消息框标题
    :param message: 消息内容
    :param type: 消息框类型（info, warning, error, yesno）
    :return: None 或 bool（仅在 yesno 类型时返回）
    """
    messagebox_window = tk.Toplevel(parent)
    messagebox_window.withdraw()  # 隐藏主窗口
    messagebox_window.attributes("-topmost", True)  # 确保置顶

    if type == "info":
        messagebox.showinfo(title, message, parent=messagebox_window)
    elif type == "warning":
        messagebox.showwarning(title, message, parent=messagebox_window)
    elif type == "error":
        messagebox.showerror(title, message, parent=messagebox_window)
    elif type == "yesno":
        return messagebox.askyesno(title, message, parent=messagebox_window)

    messagebox_window.destroy()