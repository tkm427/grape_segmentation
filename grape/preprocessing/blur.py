import cv2
import os

# フォルダ内の画像をぼかす
# kernel_size: ぼかしの強さ
def blur(input_folder_path, output_folder_path, kernel_size=5):
    for image_path in os.listdir(input_folder_path):
        image = cv2.imread(input_folder_path + image_path)
        img = cv2.blur(image, (kernel_size, kernel_size), kernel_size)
        cv2.imwrite(f'{output_folder_path}/{image_path}', img)

input_folder_path = '/mmdetection/grape/data/resize/val/color/'
output_folder_path = '/mmdetection/grape/data/resize_blur10/val/color/'
blur(input_folder_path, output_folder_path, 10)
