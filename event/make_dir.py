import os


def make_dir(folder_name):
    # 创建文件夹
    os.makedirs(folder_name, exist_ok=True)

    # 在文件夹中创建带有文件夹名称的.csv文件和.jpg文件
    file_names = ["-10X-I.csv", "-10X-H.csv", "-10X.jpg", "-100X-I.csv", "-100X-H.csv", "-100X.jpg"]
    for file_name in file_names:
        # 在文件名中添加文件夹名称
        file_base_name, extension = os.path.splitext(file_name)
        full_file_name = folder_name.split(os.path.sep)[-1] + file_base_name + extension
        open(os.path.join(folder_name, full_file_name), 'a').close()

    print(f"{folder_name}文件夹创建成功！")


if __name__ == "__main__":
    folder_names = ["20231207a-F-m1000r60T", "20231207a-F-m1500r60T", "20231207a-F-m2000r60T",
                    "20231207a-U-m1000r60T", "20231207a-U-m1500r60T", "20231207a-U-m2000r60T",
                    "20231207b-F-m1000r60T", "20231207b-F-m1500r60T", "20231207b-F-m2000r60T",
                    "20231207b-U-m1000r60T", "20231207b-U-m1500r60T", "20231207b-U-m2000r60T",
                    "20231207c-F-m1000r60T", "20231207c-F-m1500r60T", "20231207c-F-m2000r60T",
                    "20231207c-U-m1000r60T", "20231207c-U-m1500r60T", "20231207c-U-m2000r60T",
                    "20231207d-F-m1000r60T", "20231207d-F-m1500r60T", "20231207d-F-m2000r60T",
                    "20231207d-U-m1000r60T", "20231207d-U-m1500r60T", "20231207d-U-m2000r60T",
                    "20231207e-F-m1000r60T", "20231207e-F-m1500r60T", "20231207e-F-m2000r60T",
                    "20231207e-U-m1000r60T", "20231207e-U-m1500r60T", "20231207e-U-m2000r60T",
                    "20231207f-F-m1000r60T", "20231207f-F-m1500r60T", "20231207f-F-m2000r60T",
                    "20231207f-U-m1000r60T", "20231207f-U-m1500r60T", "20231207f-U-m2000r60T",
                    "20231207g-F-m1000r60T", "20231207g-F-m1500r60T", "20231207g-F-m2000r60T",
                    "20231207g-U-m1000r60T", "20231207g-U-m1500r60T", "20231207g-U-m2000r60T",
                    ]
    base_folder = "C:/Users/JiaPeng/desktop/1/文件夹"
    for folder_name in folder_names:
        full_folder_path = os.path.join(base_folder, folder_name)
        make_dir(full_folder_path)
