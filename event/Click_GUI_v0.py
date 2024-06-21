import tkinter as tk
import pyautogui
import time


# 创建一个名为root的Tk对象
root = tk.Tk()
root.title("获取鼠标位置和单击屏幕坐标")

# Flag to control whether to continue getting mouse position
get_position_flag = False
get_position_id = None

def get_mouse_position():
    global get_position_flag, get_position_id
    if get_position_flag:
        x, y = pyautogui.position()
        position_label.config(text=f"当前鼠标位置：({x}, {y})")
        get_position_id = root.after(500, get_mouse_position) # 每500毫秒获取一次鼠标位置

def single_click_on_position():
    global get_position_flag, get_position_id
    get_position_flag = False  # Stop getting mouse position
    if get_position_id is not None:
        root.after_cancel(get_position_id)  # Cancel the scheduled get_mouse_position task
    x1, y1 = map(int, position1_entry.get().split(","))
    x2, y2 = map(int, position2_entry.get().split(","))
    pyautogui.click(x=x1, y=y1)
    pyautogui.click(x=x2, y=y2)

def toggle_get_position():
    global get_position_flag
    get_position_flag = not get_position_flag
    if get_position_flag:
        get_mouse_position()

# 创建获取鼠标位置按钮
position_button = tk.Button(root, text="获取鼠标位置", command=toggle_get_position)
position_button.pack()  # 组件定位

# 创建显示鼠标位置的标签
position_label = tk.Label(root, text="当前鼠标位置：")
position_label.pack()

# 创建坐标1输入框和标签
position1_label = tk.Label(root, text="坐标1：")
position1_label.pack()

position1_entry = tk.Entry(root)
position1_entry.pack()

# 创建坐标2输入框和标签
position2_label = tk.Label(root, text="坐标2：")
position2_label.pack()

position2_entry = tk.Entry(root)
position2_entry.pack()

# 创建双击屏幕坐标按钮
click_button = tk.Button(root, text="单击屏幕坐标", command=single_click_on_position)
click_button.pack()

root.mainloop()  # Tkinter中的一个函数，它是一个事件循环，用于更新GUI的驱动程序
