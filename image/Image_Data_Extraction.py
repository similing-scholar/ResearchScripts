"""将文献图片中的曲线一次性提取出来"""

import cv2
import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt
import os
import pandas as pd


def get_image(path):
    """获取rgb图片array"""
    image = Image.open(path)
    img = np.asarray(image)
    return img


def get_box_coordinates(img, save_folder):
    """获取图片中的曲线坐标"""
    # 转换图像为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 使用Canny边缘检测
    edges = cv2.Canny(gray, 50, 150)
    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓，获取包围框的坐标
    box_coordinates = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        box_coordinates.append((x, y, x + w, y + h))

    # 遍历每个包围框并保存为单独的 PNG
    for i, (x1, y1, x2, y2) in enumerate(box_coordinates):
        # 从原始图像中裁剪感兴趣的区域
        roi = img[y1:y2, x1:x2]
        # 从裁剪的区域创建一个新的图像对象
        cropped_image = Image.fromarray(roi)
        # 将裁剪的图像保存为 PNG 文件
        cropped_image.save(os.path.join(save_folder, f'cropped_image_{i + 1}.png'))

    # 在原始图像上绘制包围框
    for box in box_coordinates:
        x1, y1, x2, y2 = box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    plt.imshow(img)
    plt.show()

    return print('cropped images saved in folder: ', save_folder)


def extract_sparse_points(img):
    """提取每一个子图中的曲线，稀疏取点，每列取一个点"""
    # 将图像从BGR颜色空间转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # 定义蓝色的HSV范围
    lower_blue = np.array([110, 100, 100])
    upper_blue = np.array([150, 255, 255])

    # 根据蓝色的HSV范围创建掩码
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 通过与原始图像进行按位与操作，保留蓝色部分
    blue_curve = cv2.bitwise_and(img, img, mask=mask)

    # 计算每一列非零值的平均坐标
    sparse_points = []
    for col in range(blue_curve.shape[1]):
        col_values = blue_curve[:, col, 0]  # 取红色通道
        non_zero_indices = np.nonzero(col_values)
        if non_zero_indices[0].size > 0:
            average_x = col
            average_y = np.mean(non_zero_indices)
            sparse_points.append([average_x, int(average_y)])

    sparse_points = np.array(sparse_points)
    return sparse_points


def interp_x(sparse_points, height):
    # 找到第一列的最大值和最小值
    sparse_points = sparse_points.astype(float)
    min_val = np.min(sparse_points[:, 0] )
    max_val = np.max(sparse_points[:, 0] )

    # 计算最大值和最小值的差值
    diff = max_val - min_val

    # 对第一列进行操作：减去最小值并除以差值
    sparse_points[:, 0] = (sparse_points[:, 0] - min_val) / diff

    sparse_points[:, 1] = 1 - sparse_points[:, 1]/height

    # 新的 x 值范围，要生成 101 个点
    new_x = np.linspace(0, 1, 101)

    # 使用 interp 函数进行线性插值
    new_y = np.interp(new_x, sparse_points[:, 0], sparse_points[:, 1])
    return new_y


if __name__ == '__main__':
    # 1. 读取原始图片做分割
    image_path = 'C:/Users/JiaPeng/Desktop/test/Image 3.png'
    save_folder = 'C:/Users/JiaPeng/Desktop/1/crop'
    # img = get_image(image_path)
    # get_box_coordinates(img, save_folder)

    # 2. 读取分割后的图片做稀疏取点
    df = pd.DataFrame({'wave_length_index': np.linspace(0, 1, 101)})
    # 获取文件夹中所有PNG图片的文件名
    png_files = [f for f in os.listdir(save_folder) if f.endswith('.png')]
    # 遍历每个PNG文件
    for png_file in png_files:
        # 读取PNG文件
        png_path = os.path.join(save_folder, png_file)
        img = get_image(png_path)
        # 提取稀疏点
        sparse_points = extract_sparse_points(img)
        new_y = interp_x(sparse_points, img.shape[0])
        # 创建新的列
        df[png_file] = new_y
    df.to_excel(os.path.join(save_folder, 'data_extraction.xlsx'), sheet_name='Transmittance', index=False)

