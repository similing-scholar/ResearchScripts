import tkinter as tk
import pyautogui
import time
import pyperclip


class AutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("软件联用脚本v1--习武的书生")

        self.get_position_flag = False  # 用于控制是否继续获取鼠标位置的标志
        self.get_position_id = None  # 用于存储get_mouse_position的任务id

        self.setup_ui()

    def setup_ui(self):
        tk.Button(self.root, text="获取鼠标坐标与颜色", command=self.toggle_get_position).pack()
        self.position_label = tk.Label(self.root, text="当前鼠标坐标与颜色:")
        self.position_label.pack()

        self.position_entries = []  # 存储坐标输入框
        self.clicks_entries = []  # 存储点击次数输入框
        self.color_entries = []  # 存储颜色匹配输入框

        self.setup_position_frame("开始坐标1(点击):", True)
        self.setup_delay_frame()  # 坐标1与坐标2之间的延迟时间
        self.setup_position_frame("开始坐标2(点击):", True)
        self.setup_position_frame("结束坐标1(监控):", False, color=True)
        self.setup_position_frame("结束坐标2(点击):", True)

        tk.Button(self.root, text="开始执行逻辑", command=self.single_click_on_positions).pack()

    def setup_position_frame(self, label_text, include_clicks, color=False):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)

        tk.Label(frame, text=label_text).pack(side=tk.LEFT)
        position_entry = tk.Entry(frame, width=8)
        position_entry.pack(side=tk.LEFT, padx=5)
        self.position_entries.append(position_entry)

        if include_clicks:
            tk.Label(frame, text="点击次数:").pack(side=tk.LEFT)
            clicks_entry = tk.Entry(frame, width=3)
            clicks_entry.pack(side=tk.LEFT)
            self.clicks_entries.append(clicks_entry)
        else:
            self.clicks_entries.append(None)

        if color:
            tk.Label(frame, text="监控RGB:").pack(side=tk.LEFT)
            color_entry = tk.Entry(frame, width=10)
            color_entry.pack(side=tk.LEFT)
            self.color_entries.append(color_entry)
        else:
            self.color_entries.append(None)

    def setup_delay_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X)
        tk.Label(frame, text="间隔时间(s):").pack(side=tk.LEFT)
        self.delay_entry = tk.Entry(frame, width=5)
        self.delay_entry.pack(side=tk.LEFT)

    def get_mouse_position(self):
        if self.get_position_flag:
            x, y = pyautogui.position()
            current_color = pyautogui.pixel(x, y)
            self.position_label.config(text=f"坐标:({x}, {y}), 颜色:{current_color}")
            coordinates = f"{x}, {y}"
            pyperclip.copy(coordinates)
            self.get_position_id = self.root.after(500, self.get_mouse_position)

    def single_click_on_positions(self):
        self.get_position_flag = False  # 首先确保停止当前正在进行的获取鼠标位置的操作
        if self.get_position_id is not None:
            self.root.after_cancel(self.get_position_id)  # 取消已开始的获取鼠标位置任务

        # 从界面获取用户设置的延迟时间，如果没有输入则默认为0
        delay_time = float(self.delay_entry.get()) if self.delay_entry.get() else 0

        # 遍历所有的坐标输入框
        for i, entry in enumerate(self.position_entries):
            if entry is not None and self.clicks_entries[i] is not None:
                x, y = map(int, entry.get().split(","))
                n = int(self.clicks_entries[i].get())
                pyautogui.click(x=x, y=y, clicks=n)  # 使用pyautogui库执行点击操作，点击次数为n
                if i == 0:  # 在第一坐标点击后应用延迟
                    time.sleep(delay_time)
                # 只遍历开始的坐标
                if i == 1:
                    break

        # 在所有开始按钮点击后，加一个延时防止颜色检查过快
        time.sleep(2)
        self.check_color_and_click()

    def check_color_and_click(self):
        x3, y3 = map(int, self.position_entries[2].get().split(","))
        x4, y4 = map(int, self.position_entries[3].get().split(","))
        n4 = int(self.clicks_entries[3].get())
        monitor_color = tuple(map(int, self.color_entries[2].get().split(',')))

        current_color = pyautogui.pixel(x3, y3)
        if current_color == monitor_color:
            pyautogui.click(x=x4, y=y4, clicks=n4)
        else:
            self.root.after(500, self.check_color_and_click)  # 结束与开始的延迟

    def toggle_get_position(self):
        self.get_position_flag = not self.get_position_flag
        if self.get_position_flag:
            self.get_mouse_position()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()
