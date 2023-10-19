"""
将图片名称添加到图片左上角
"""
from PIL import Image, ImageDraw, ImageFont
import os


def add_text_to_images(folder_path):
    # 获取文件夹中所有的PNG文件
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # 设置文本颜色和字体
    text_color = (255, 0, 0)
    # 指定自定义字体文件路径
    font_path = 'C:/Windows/Fonts/simhei.ttf'
    font_size = 36
    # 创建字体对象
    font = ImageFont.truetype(font_path, font_size)

    # 循环处理每个PNG文件
    for png_file in png_files:
        # 打开图片
        image = Image.open(os.path.join(folder_path, png_file))
        # 创建绘图对象
        draw = ImageDraw.Draw(image)

        # 获取图片名称（不带文件扩展名）
        image_name = os.path.splitext(png_file)[0].split('_')[0]
        # 在左上角添加文本
        draw.text((10, 10), image_name, fill=text_color, font=font)

        # 保存带有文本的图片
        image.save(os.path.join(folder_path, png_file))
        # 关闭图片
        image.close()
        print(f'已添加文本到{png_file}')
    return print('end')


if __name__ == '__main__':
    folder_path = 'D:/BIT课题研究/微型光谱成像仪/【数据】导电聚合物数据/郁海凡登记/20230828数据/film/显微/all_images'
    add_text_to_images(folder_path)

