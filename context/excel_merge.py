"""
合并excel内容到新的excel中
"""
import os
import pandas as pd


def merge_text2excel(folder_path, result_path):
    # 创建一个空的DataFrame，用于存储提取的数据
    result_df = pd.DataFrame(columns=['Film Name', 'center_x', 'center_y', 'radius (pixel)', 'scale (mm/pixel)'])

    # 获取文件夹中的所有Excel文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx'):
            # 读取Excel文件
            file_path = os.path.join(folder_path, filename)
            excel_data = pd.read_excel(file_path, sheet_name='circle')

            # 提取文件名
            film_name = filename.split('.')[0].split('_')[0]

            # 提取数据
            center_x = excel_data['center(x, y)'].iloc[0]
            center_y = excel_data['center(x, y)'].iloc[1]
            radius_pixel = excel_data['radius (pixel)'].iloc[0]
            scale_mm_pixel = excel_data['scale (mm/pixel)'].iloc[0]

            # 将提取的数据添加到结果DataFrame
            result_df = result_df.append(
                {'Film Name': film_name, 'center_x': center_x, 'center_y': center_y, 'radius (pixel)': radius_pixel,
                 'scale (mm/pixel)': scale_mm_pixel}, ignore_index=True)

    # 将结果保存为新的Excel文件
    result_df.to_excel(result_path, index=False)
    return print(f'提取的数据已保存到{result_path}')


def update_excel_with_image_paths(file_path, image_folder):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 遍历每一行并添加 "image_path" 列
    for index, row in df.iterrows():
        film_name = row['Film Name']
        image_name = film_name + '.png'
        image_path = os.path.join(image_folder, image_name)

        # 将生成的图片路径添加到 "image_path" 列
        df.loc[index, 'image_path'] = image_path

    # 将数据帧保存回原始Excel文件（覆盖原文件）
    df.to_excel(file_path, index=False)
    return print("Image paths are added")



if __name__ == '__main__':
    folder_path = 'D:/BIT课题研究/微型光谱成像仪/【数据】导电聚合物数据/郁海凡登记/20231007/solution/层析板/single/RadialProfile'
    result_path = 'D:/BIT课题研究/微型光谱成像仪/【数据】导电聚合物数据/郁海凡登记/20231007/solution/层析板/single/RadialProfile_merge.xlsx'
    # merge_text2excel(folder_path, result_path)

    image_folder = 'D:/BIT课题研究/微型光谱成像仪/【数据】导电聚合物数据/郁海凡登记/20231007/solution/层析板/single/image'
    update_excel_with_image_paths(result_path, image_folder)



