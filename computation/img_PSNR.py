"""
峰值信噪比计算
"""
import glob
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


def PSNR(img1,img2):
    # 强制转换元素类型，为了运算
    width = img1.shape[0]
    height = img1.shape[1]
    img1 = img1.astype(np.int32)
    img2 = img2.astype(np.int32)

    #计算均方误差,初始化64位无符号整型，防止累加中溢出
    mse = np.uint64(0)
    for i in range(width):
        for j in range(height):
            mse += (img1[i][j] - img2[i][j]) ** 2
    mse /= (width * height)
    if mse == 0:
        return 100
    psnr = 10 * math.log10((255 ** 2) / mse)

    return psnr


def main():
    image_o = Image.open('D:/BIT课题研究/荧光膜加密/pic/熵计算/20220106/明文(45,45,45).png')  # 原图
    img_o = np.asarray(image_o)
    r_o, g_o, b_o, _ = cv2.split(img_o)
    image_j = Image.open('D:/BIT课题研究/荧光膜加密/pic/噪声/高斯噪声/高斯攻击解密.png')  # 解密
    img_j = np.asarray(image_j)
    r_j, g_j, b_j, _ = cv2.split(img_j)
    for (c1, c2) in [(r_o, r_j), (g_o, g_j), (b_o, b_j)]:
        psnr = PSNR(c1, c2)
        print('{:.4f}'.format(psnr))

    return None


if __name__ == '__main__':
    main()