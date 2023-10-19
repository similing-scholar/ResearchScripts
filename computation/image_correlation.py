"""图像相邻像素相关性计算"""
import glob
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np
import matplotlib.pyplot as plt


def correlation(img):
    N = 1000  # 统计像素个数
    pic_width = img.shape[0]
    pic_height = img.shape[1]

    # 统计x，y坐标值
    x_row_col = []  # x坐标
    x = []  # x像素值
    y_horizontal = []  # 水平相邻像素值
    y_vertical = []  # 垂直相邻像素值
    y_diagonal = []  # 对角相邻像素值

    for i in range(N):  # 随机选点
        # 随机产生一个[0,w-1),[0,h-1)范围内的坐标，最后一行/列不选做原始x坐标
        rndrow, rndcol = (np.random.randint(0, pic_width - 1), np.random.randint(0, pic_height - 1))
        while (rndrow, rndcol) in x_row_col:  # 不选重复原始x坐标
            rndrow, rndcol = (np.random.randint(0, pic_width - 1), np.random.randint(0, pic_height - 1))
        else:
            x_row_col.append((rndrow, rndcol))  # x坐标序列对
            x.append(img[rndrow][rndcol])
            y_horizontal.append(img[rndrow][rndcol + 1])  # 右侧像素
            y_vertical.append(img[rndrow + 1][rndcol])  # 下方像素
            y_diagonal.append(img[rndrow + 1][rndcol + 1])  # 右下对角

    # 合并所有x,y值，做scatter图
    x = x * 3
    y = y_horizontal + y_vertical + y_diagonal
    # plt.scatter(x, y)
    # plt.show()

    # 计算x均值与方差
    Ex = np.mean(x)
    Dx = np.var(x, ddof=0)  # 底数N，有偏估计

    # 计算y均值与方差
    Ey_h = np.mean(y_horizontal)  # 水平
    Dy_h = np.var(y_horizontal, ddof=0)
    Ey_v = np.mean(y_vertical)  # 垂直
    Dy_v = np.var(y_vertical, ddof=0)
    Ey_d = np.mean(y_diagonal)  # 对角
    Dy_d = np.var(y_diagonal, ddof=0)

    # 计算x,y协方差
    cov_xyh = 0  # 水平
    for i in range(N):
        cov_xyh = cov_xyh + (x[i] - Ex) * (y_horizontal[i] - Ey_h)
    cov_xyh = cov_xyh / N

    cov_xyv = 0  # 垂直
    for i in range(N):
        cov_xyv = cov_xyv + (x[i] - Ex) * (y_vertical[i] - Ey_v)
    cov_xyv = cov_xyv / N

    cov_xyd = 0  # 对角
    for i in range(N):
        cov_xyd = cov_xyd + (x[i] - Ex) * (y_diagonal[i] - Ey_d)
    cov_xyd = cov_xyd / N

    # 计算相关系数
    Rx_yh = cov_xyh / (np.sqrt(Dx) * np.sqrt(Dy_h))
    Rx_yv = cov_xyv / (np.sqrt(Dx) * np.sqrt(Dy_v))
    Rx_yd = cov_xyd / (np.sqrt(Dx) * np.sqrt(Dy_d))

    return Rx_yh, Rx_yv, Rx_yd, x, y


def main():
    path = 'D:/BIT课题研究/荧光膜加密/pic/熵计算/20220106/多色密文(45,300).png'
    image = Image.open(path)
    img = np.asarray(image)
    imgr, imgg, imgb, _ = cv2.split(img)
    for (c, color) in [(imgr, 'red'), (imgg, 'green'), (imgb, 'blue')]:
        Rx_yh, Rx_yv, Rx_yd, x, y = correlation(c)
        print('{}通道:水平{:.4f},垂直{:.4f},对角{:.4f}'.format(color, Rx_yh, Rx_yv, Rx_yd))
        plt.figure()
        plt.scatter(x, y, s=1, c=color)
        plt.show()
    return None


if __name__ == '__main__':
    main()