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
    # 创建一个新的顶层窗口并隐藏
    messagebox_window = tk.Toplevel(parent)
    messagebox_window.withdraw()  
    messagebox_window.attributes("-topmost", True)  # 确保置顶

    # 根据消息框类型显示相应的消息框
    messagebox_func = {
        "info": messagebox.showinfo,
        "warning": messagebox.showwarning,
        "error": messagebox.showerror,
        "yesno": messagebox.askyesno,
    }.get(type)

    if messagebox_func:
        result = messagebox_func(title, message, parent=messagebox_window)
        # 如果是 yesno 类型，返回结果
        if type == "yesno":
            return result

    messagebox_window.destroy()
