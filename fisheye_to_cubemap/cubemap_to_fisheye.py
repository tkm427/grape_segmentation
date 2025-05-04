# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import vrProjector
import cv2


def cubemap_to_fisheye(input_img, output_img):        
    side = 'right'
    img_size = 480

    if( (side != 'right') and (side !='left') ):
        print( '3rd argument must be "right" or "left"' ) 
        sys.exit()

    #読み込み画像と同じサイズの真っ黒な画像を作成
    cube_right = cv2.imread( input_img, cv2.IMREAD_COLOR )

    #画像サイズは基本正方形だということにしておいて，画像ファイルがないようであれば作る
    blank_file = 'blank_' + str(cube_right.shape[0]) + '.png'

    #blank ファイルがない場合，作って保存
    if not( os.path.isfile(blank_file)):
        blank_image = np.zeros((cube_right.shape[0],cube_right.shape[1], 3), np.uint8)
        cv2.imwrite( blank_file, blank_image )

    #キューブマップ読み込み
    source2 = vrProjector.CubemapProjection()
    if side == 'right':
        source2.loadImages( blank_file, input_img, blank_file, blank_file, blank_file, blank_file)
    else:
        source2.loadImages( blank_file, blank_file, blank_file, input_img, blank_file, blank_file)
        
    out2 = vrProjector.SideBySideFisheyeProjection()
    #サイズはもとに戻す．
    out2.initImage( img_size*2, img_size)
    out2.reprojectToThis(source2)
    #片方だけ保存
    out2.saveImage_half( output_img, side )

def cubemap_to_fisheye_folder(input_folder, output_folder):
    for image_path in os.listdir(input_folder):
        cubemap_to_fisheye(input_folder + image_path, output_folder + image_path)

input_folder = '/mmdetection/grape/data/cubemap/'
output_folder = '/mmdetection/grape/data/fisheye/'
cubemap_to_fisheye_folder(input_folder, output_folder)
