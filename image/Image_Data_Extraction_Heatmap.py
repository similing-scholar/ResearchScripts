import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
import pandas as pd


def extract_precise_colorbar_mapping(colorbar_path, colorbar_min, colorbar_max, divisions=100):
    """
    将colorbar分为指定份数，并提取颜色与数值的映射关系
    """
    # 加载 colorbar 图像
    colorbar_img = Image.open(colorbar_path).convert("RGB")
    colorbar_data = np.array(colorbar_img)

    # 提取中间列的颜色值
    colors = colorbar_data[:, colorbar_data.shape[1] // 2, :]

    # 确保分为指定的 divisions 数量
    sampled_indices = np.linspace(0, len(colors) - 1, divisions, dtype=int)
    sampled_colors = colors[sampled_indices]

    # 生成线性数值范围
    values = np.linspace(colorbar_min, colorbar_max, divisions)

    # 构建颜色到数值的映射关系
    color_mapping = {tuple(color): value for color, value in zip(sampled_colors, values)}
    return color_mapping


def resize_heatmap(heatmap_path, target_shape):
    """
    调整热力图大小
    """
    heatmap_img = Image.open(heatmap_path).convert("RGB")
    resized_img = heatmap_img.resize(target_shape, Image.NEAREST)  # 使用最近邻插值
    return np.array(resized_img)


def map_heatmap_with_nearest_color(resized_heatmap, color_mapping):
    """
    使用近似匹配方法将热力图颜色映射到colorbar数值
    """
    # 提取colorbar颜色和对应数值
    color_values = np.array(list(color_mapping.keys()))
    mapped_values = list(color_mapping.values())

    # 构建KDTree进行快速最近邻搜索
    tree = KDTree(color_values)

    # 初始化数值矩阵
    heatmap_values = np.zeros((resized_heatmap.shape[1], resized_heatmap.shape[0]))

    # 遍历每个像素，找到最近的颜色值
    for i in range(resized_heatmap.shape[1]):  # 行
        for j in range(resized_heatmap.shape[0]):  # 列
            pixel = tuple(resized_heatmap[j, i])  # 提取像素颜色
            _, idx = tree.query(pixel)  # 查找最近的颜色索引
            heatmap_values[i, j] = mapped_values[idx]  # 赋值

    return heatmap_values


# ==============================
# 参数设置
# ==============================
heatmap_path = "C:/Users/JiaPeng/Desktop/test/20241215heatmap/light/2024-12-16 10 44 30.png"  # 热力图路径
colorbar_path = "C:/Users/JiaPeng/Desktop/test/20241215heatmap/light/2024-12-16 10 44 58.png"  # colorbar路径
colorbar_min = 1  # colorbar 最小值 貌似写反了？？
colorbar_max = 0   # colorbar 最大值
target_shape = (100, 40)  # 调整热力图为 50x20 的形状

# ==============================
# 执行流程
# ==============================
# 1. 提取 colorbar 颜色与数值映射
precise_color_mapping = extract_precise_colorbar_mapping(colorbar_path, colorbar_min, colorbar_max, divisions=200)

# 2. 调整热力图大小
resized_heatmap = resize_heatmap(heatmap_path, target_shape)

# 3. 近似匹配热力图颜色到数值
approximate_heatmap_values = map_heatmap_with_nearest_color(resized_heatmap, precise_color_mapping)

# 转置矩阵，确保行和列方向一致
adjusted_heatmap_values = approximate_heatmap_values.T

# 显示修正后的热力图
plt.imshow(adjusted_heatmap_values, cmap='coolwarm', aspect='auto', origin='lower')
plt.colorbar(label='Value')
plt.title('Heatmap Mapped Using Approximate Nearest Color (Corrected)')
plt.xlabel('Columns (50)')
plt.ylabel('Rows (20)')
plt.show()

# 将列逆序
reversed_heatmap_values = approximate_heatmap_values[:, ::-1]
df = pd.DataFrame(reversed_heatmap_values)

df.to_csv("C:/Users/JiaPeng/Desktop/test/20241215heatmap/light/heatmap_values.csv", index=False)
print("热力图数值矩阵已保存为 heatmap_values.csv")