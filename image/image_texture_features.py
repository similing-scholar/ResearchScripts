import os
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.feature import graycomatrix, graycoprops

def process_image(file_path, file_name):
    # 读取图像
    image = Image.open(file_path)
    # 将图像转换为NumPy数组
    image = np.array(image)
    # 获取图像的尺寸
    height, width, _ = image.shape
    # 计算裁剪区域的尺寸
    crop_height = int(height * 0.5)
    crop_width = int(width * 0.5)
    # 计算裁剪区域的起始位置
    start_row = int((height - crop_height) / 2)
    start_col = int((width - crop_width) / 2)
    # 裁剪图像
    cropped_image = image[start_row:start_row + crop_height, start_col:start_col + crop_width]
    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2GRAY)
    # 输出裁剪后的图像
    cropped_file_path = os.path.splitext(file_path)[0] + "_cropped.png"
    cropped_image_pil = Image.fromarray(cropped_image)
    cropped_image_pil.save(cropped_file_path)
    # 输出裁剪后的灰度图像
    cropped_gray_file_path = os.path.splitext(file_path)[0] + "_cropped_gray.png"
    gray_image_pil = Image.fromarray(gray_image)
    gray_image_pil.save(cropped_gray_file_path)

    # 提取灰度共生矩阵
    glcm = graycomatrix(gray_image, distances=[5], angles=[0], levels=256, symmetric=True, normed=True)
    # 提取纹理特征
    contrast = graycoprops(glcm, 'contrast')[0][0]
    dissimilarity = graycoprops(glcm, 'dissimilarity')[0][0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0][0]
    energy = graycoprops(glcm, 'energy')[0][0]
    correlation = graycoprops(glcm, 'correlation')[0][0]
    # 打印纹理特征
    print("File:", file_name, "Contrast:", contrast, "Dissimilarity:", dissimilarity, "Homogeneity:", homogeneity,
          "Energy:", energy, "Correlation:", correlation)
    # 显示灰度共生矩阵的热图
    plt.imshow(glcm[:, :, 0, 0], cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('GLCM Heatmap')
    plt.xlabel('Gray Level')
    plt.ylabel('Gray Level')
    glcm_file_path = os.path.splitext(file_path)[0] + "_glcm.png"
    plt.savefig(glcm_file_path)
    plt.close()

    return None

# 处理文件夹下的所有图片
folder_path = 'D:/BIT课题研究/微型光谱成像仪/【数据】导电聚合物数据/郁海凡论文数据/小分子酸'
for file_name in os.listdir(folder_path):
    if file_name.endswith('.png'):
        file_path = os.path.join(folder_path, file_name)
        process_image(file_path, file_name)