import cv2
import numpy as np
import time
import cvui

# 初始化cvui
cvui.init('Camera')

def update_exposure(val):
    exposure = val - 13  # 将滑动条值转换为相机可以接受的曝光值范围
    cap.set(cv2.CAP_PROP_EXPOSURE, float(exposure))
    print(f"曝光时间设置为: {exposure}")

def draw_text(frame, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.5, color=(255, 255, 255), thickness=1):
    cv2.putText(frame, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

def ensure_valid_extension(filename):
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    if not any(filename.lower().endswith(ext) for ext in valid_extensions):
        return filename + '.png'  # 默认使用.png扩展名
    return filename

# 打开USB相机
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("无法打开相机")
    exit()

# 设置MJPG编码格式
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
cap.set(cv2.CAP_PROP_FOURCC, fourcc)

# 创建窗口和滑动条
cv2.namedWindow('Camera')
cv2.createTrackbar('Exposure', 'Camera', 0, 13, update_exposure)

# 初始化曝光时间
initial_exposure = int(cap.get(cv2.CAP_PROP_EXPOSURE)) + 13
cv2.setTrackbarPos('Exposure', 'Camera', initial_exposure)

prev_time = None
fps = 0
original_frame = None

# 设置文件名输入框初始值
filename_input = 'captured_image'

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取帧")
        break

    # 保存原始帧以用于保存图像
    original_frame = frame.copy()

    # 计算实际FPS
    curr_time = time.time()
    if prev_time is not None:
        fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # 获取相机参数
    try:
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
        contrast = cap.get(cv2.CAP_PROP_CONTRAST)
        saturation = cap.get(cv2.CAP_PROP_SATURATION)
        hue = cap.get(cv2.CAP_PROP_HUE)
        gain = cap.get(cv2.CAP_PROP_GAIN)
        exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    except Exception as e:
        print(f"Error retrieving camera parameters: {e}")
        continue

    # 计算RGB均值和方差
    mean, stddev = cv2.meanStdDev(frame)
    mean_rgb = mean.flatten()
    stddev_rgb = stddev.flatten()

    # 绘制参数和统计数据
    draw_text(frame, f"Width: {frame_width}", (10, 20))
    draw_text(frame, f"Height: {frame_height}", (10, 40))
    draw_text(frame, f"FPS: {fps:.2f}", (10, 60))
    draw_text(frame, f"Brightness: {brightness}", (10, 80))
    draw_text(frame, f"Contrast: {contrast}", (10, 100))
    draw_text(frame, f"Saturation: {saturation}", (10, 120))
    draw_text(frame, f"Hue: {hue}", (10, 140))
    draw_text(frame, f"Gain: {gain}", (10, 160))
    draw_text(frame, f"Exposure: {exposure}", (10, 180))
    draw_text(frame, f"Mean RGB: {mean_rgb}", (10, 200))
    draw_text(frame, f"StdDev RGB: {stddev_rgb}", (10, 220))

    # 创建保存按钮和输入框
    frame_copy = frame.copy()
    cvui.text(frame_copy, 10, 240, "Filename:")
    cvui.rect(frame_copy, 100, 240, 200, 30, 0xff0000)
    cvui.text(frame_copy, 110, 260, filename_input)

    if cvui.button(frame_copy, 320, 240, "Save Image"):
        # 从输入框获取文件名并保存原始图像
        filename_input = ensure_valid_extension(filename_input)
        output_filename = f'C:/Users/JiaPeng/Desktop/test/{filename_input}'
        cv2.imwrite(output_filename, original_frame)
        print(f"图像已保存为 {output_filename}")

    # 显示图像和按钮
    cvui.update('Camera')
    cv2.imshow('Camera', frame_copy)

    # 处理键盘输入
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 'esc' 键
        break
    elif key == 8:  # 'backspace' 键
        filename_input = filename_input[:-1]
    elif key != 255:  # 其他字符
        filename_input += chr(key)

# 释放相机并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
