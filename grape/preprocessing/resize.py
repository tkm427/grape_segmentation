import cv2
import os

# フォルダ内の画像をリサイズ
def resize(image_folder_path, output_folder_path):
    for image_path in os.listdir(image_folder_path):
        # 画像読み込み
        image = cv2.imread(image_folder_path + image_path)
        height, width = image.shape[:2]
        w = 900
        # img[top : bottom, left : right]
        img = image[height // 2 - w // 2 : height // 2 + w // 2, width // 2 - w // 2 : width // 2 + w // 2]
        # 縮小
        img_resize = cv2.resize(img, (480, 480))
        cv2.imwrite(f'{output_folder_path}/{image_path}', img_resize)

image_folder_path = '/mmdetection/grape/data/fastgrape/grape/fuji/train/color/'
output_folder_path = '/mmdetection/grape/data/resize/train/color/'
resize(image_folder_path, output_folder_path)