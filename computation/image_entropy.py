"""
图像熵计算
"""
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np


def pic_entropy_1D(img):  # 一维灰度熵
    # 读取图片基本信息
    width = img.shape[0]
    height = img.shape[1]

    # 计算灰阶出现概率
    hist_cv = cv2.calcHist([img], [0], None, [256], [0, 256])
    P = hist_cv / (width * height)  # 概率

    # 计算1D灰度熵
    H = 0  # 初始化熵
    for p in P:
        if p == 0:  # 0不能做分母
            H = H
        else:
            H = H + p * np.log2(1/p)

    return H[0]  # calcHist返回值导致H为列表


def pic_entropy_2D(img):  # 二维灰度熵
    # 读取图片基本信息
    width = img.shape[0]
    height = img.shape[1]

    # 3*3邻域计算邻域平均灰度值
    IJ = []  # (i,j)二元组
    N = 1  # i像素
    for row in range(width):  # 行
        for col in range(height):  # 列
            Left_x = np.max([0, col - N])  # 判断是否左边线，是边线就选择0
            Right_x = np.min([height, col + N + 1])  # 右边线
            up_y = np.max([0, row - N])  # 上边线
            down_y = np.min([width, row + N + 1])  # 下边线
            region = img[up_y:down_y, Left_x:Right_x]  # 九宫格区域
            j = (np.sum(region) - img[row][col]) / (region.shape[0]*region.shape[1] - 1)
            IJ.append([img[row][col], j])
    # print(ij)

    # 计算f(i,j)
    newIJ = []  # 去重后的列表
    for ij in IJ:
        if ij not in newIJ:
            newIJ.append(ij)
    F = []  # 出现频数
    for ij in newIJ:
        F.append(IJ.count(ij))

    # 计算概率
    P = []
    for f in F:
        p = f / (width * height)
        P.append(p)

    # 计算2D灰度熵
    H = 0
    for p in P:
        if p == 0:
            H = H
        else:
            H = H + p * np.log2(1/p)

    return H


def main():
    # 1.1 地址获取图片
    path = 'D:/BIT课题研究/荧光膜加密/pic/熵计算/20220106/多色解密2.png'
    image = Image.open(path)
    img = np.asarray(image)

    # 1.2 创建图片
    # a = [i for i in range(256)]
    # img = np.array(a).astype(np.uint8).reshape(16, 16)

    # 2. 拆分通道
    imgr, imgg, imgb, _ = cv2.split(img)

    # 3. 计算熵
    print('一维熵')
    for c in [imgr, imgg, imgb]:
        H = pic_entropy_1D(c)
        print('{:.4f}'.format(H))

    print('二维熵')
    for c in [imgr, imgg, imgb]:
        H = pic_entropy_2D(c)
        print('{:.4f}'.format(H))

    return None


if __name__ == '__main__':
    # pic_entropy_1D()
    # pic_entropy_2D()
    main()