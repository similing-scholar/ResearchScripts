import cv2
import time


def capture_image(camera, save_path):
    # 读取一帧图像
    ret, frame = camera.read()
    if ret:
        # 保存图像
        cv2.imwrite(save_path, frame)
        print("图片已保存：", save_path)
    else:
        print("无法读取摄像头图像")


def main():
    # 打开摄像头
    camera = cv2.VideoCapture(0)

    # 设置定时拍照间隔（秒）
    interval = 0.01  # 【修改】
    elapsed_time = 0  # 已经过去的时间

    while True:
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        elapsed_minutes = elapsed_time // 60
        elapsed_seconds = elapsed_time % 60

        # 生成保存路径
        main_path = "C:/Users/JiaPeng/Desktop/test/image/"  # 【修改】
        pic_name = f"{elapsed_minutes}min_{elapsed_seconds}s_{current_time}.jpg"
        save_path = main_path + pic_name

        # 更新已经过去的时间
        elapsed_time += interval

        # 拍照并保存图片
        capture_image(camera, save_path)

        # 等待一段时间
        time.sleep(interval)

        # 检查键盘输入
        if cv2.waitKey(1) == 27:  # ESC 键的 ASCII 值为 27
            break

    # 关闭摄像头
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
