import tkinter as tk
import pyautogui
import time
import pyperclip


root = tk.Tk()
root.title("获取鼠标位置和单击屏幕坐标")
# 用于控制是否继续获取鼠标位置的标志
get_position_flag = False
get_position_id = None


def get_mouse_position():
    global get_position_flag, get_position_id
    if get_position_flag:
        x, y = pyautogui.position()
        current_color = pyautogui.pixel(x, y)
        position_label.config(text=f"位置:({x}, {y}), color: {current_color}")
        # 将鼠标位置复制到剪贴板

        coordinates = f"{x}, {y}"
        pyperclip.copy(coordinates)
        # 每500毫秒获取一次鼠标位置
        get_position_id = root.after(500, get_mouse_position)


def single_click_on_positions():
    global get_position_flag, get_position_id
    get_position_flag = False  # 停止get_mouse_position
    if get_position_id is not None:
        root.after_cancel(get_position_id)  # 取消计划的get_mouse_position任务
    x1, y1 = map(int, position1_entry.get().split(","))
    x2, y2 = map(int, position2_entry.get().split(","))
    x3, y3 = map(int, position3_entry.get().split(","))
    x4, y4 = map(int, position4_entry.get().split(","))

    pyautogui.click(x=x1, y=y1)
    pyautogui.click(x=x2, y=y2)

    time.sleep(2)
    check_color_and_click(x3, y3, x4, y4)


def check_color_and_click(x3, y3, x4, y4):
    current_color = pyautogui.pixel(x3, y3)
    if current_color == (240, 240, 240):  # 【修改】
        # print(f"颜色变化！当前颜色: {current_color}")
        pyautogui.click(x=x4, y=y4)
    else:
        # print(f"{x3, y3}颜色未变化，当前颜色: {current_color}")
        root.after(500, check_color_and_click, x3, y3, x4, y4)


def toggle_get_position():
    global get_position_flag
    get_position_flag = not get_position_flag
    if get_position_flag:
        get_mouse_position()


position_button = tk.Button(root, text="获取鼠标位置", command=toggle_get_position)
position_button.pack()

position_label = tk.Label(root, text="当前鼠标位置：")
position_label.pack()

position1_label = tk.Label(root, text="坐标1（软件a的开始按钮）：")
position1_label.pack()

position1_entry = tk.Entry(root)
position1_entry.pack()

position2_label = tk.Label(root, text="坐标2（软件b的开始按钮）：")
position2_label.pack()

position2_entry = tk.Entry(root)
position2_entry.pack()

position3_label = tk.Label(root, text="坐标3（软件b的结束按钮）：")
position3_label.pack()

position3_entry = tk.Entry(root)
position3_entry.pack()

position4_label = tk.Label(root, text="坐标4（软件a的结束按钮）：")
position4_label.pack()

position4_entry = tk.Entry(root)
position4_entry.pack()

click_button = tk.Button(root, text="单击屏幕坐标", command=single_click_on_positions)
click_button.pack()

root.mainloop()  # Tkinter中的一个函数，它是一个事件循环，用于更新GUI的驱动程序
