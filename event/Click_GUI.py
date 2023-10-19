import tkinter as tk
import pyautogui


def get_mouse_position():
    # 获取当前鼠标位置并更新position_label的文本
    x, y = pyautogui.position()
    position_label.config(text=f"当前鼠标位置：({x}, {y})")
    root.after(500, get_mouse_position) # 每500毫秒获取一次鼠标位置

def double_click_on_position():
    # 获取position1_entry和position2_entry中的坐标，并在这些坐标上双击
    x1, y1 = map(int, position1_entry.get().split(","))
    x2, y2 = map(int, position2_entry.get().split(","))
    pyautogui.doubleClick(x=x1, y=y1)
    pyautogui.doubleClick(x=x2, y=y2)


# 创建一个名为root的Tk对象
root = tk.Tk()
root.title("获取鼠标位置和双击屏幕坐标")

# 创建获取鼠标位置按钮
position_button = tk.Button(root, text="获取鼠标位置", command=get_mouse_position)
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
click_button = tk.Button(root, text="双击屏幕坐标", command=double_click_on_position)
click_button.pack()

root.mainloop()  # Tkinter中的一个函数，它是一个事件循环，用于更新GUI的驱动程序