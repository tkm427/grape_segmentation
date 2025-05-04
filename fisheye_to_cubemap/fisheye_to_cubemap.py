import sys
import os 
import numpy as np
import vrProjector
import cv2

#画像の読み込み.入力画像が左側か右側か知っておく必要あり．
def fisheye_to_cubemap(input_img, output_img):
    # 入力画像が右側
    side = 'right'
    img_size = 480


    if( (side != 'right') and (side !='left') ):
        print( '3rd argument must be "right" or "left"' ) 
        sys.exit()

    fisheye_raw = cv2.imread( input_img, cv2.IMREAD_COLOR )
    blanc_img = np.zeros( (fisheye_raw.shape[0], fisheye_raw.shape[1], 3 ), np.uint8 )
    dualfisheye = []
    if side == 'right':
        #左側に真っ黒な部分をくっつけて画像を作成
        dualfisheye = cv2.hconcat( [blanc_img, fisheye_raw ] )
    else:
        dualfisheye = cv2.hconcat( [blanc_img, fisheye_raw ] )
    #一時保存
    cv2.imwrite( 'dualfish_fix.png', dualfisheye )

    #キューブマップにしてみる
    source = vrProjector.SideBySideFisheyeProjection()
    source.loadImage('dualfish_fix.png')

    out = vrProjector.CubemapProjection()
    out.initImages(img_size,img_size)
    out.reprojectToThis(source)

    if( side == 'right' ):
        out.saveImages("front.png", output_img, "back.png", "left.png", "top.png", "bottom.png")
    else:
        out.saveImages("front.png", "right.png", "back.png", output_img, "top.png", "bottom.png")

def fisheye_to_cubemap_folder(input_folder, output_folder):
    for image_path in os.listdir(input_folder):
        fisheye_to_cubemap(input_folder + image_path, output_folder + image_path)

input_folder = '/mmdetection/grape/data/fisheye/'
output_folder = '/mmdetection/grape/data/cubemap/'
fisheye_to_cubemap_folder(input_folder, output_folder)