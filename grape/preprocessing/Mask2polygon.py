from PIL import Image
import numpy as np
from skimage import measure
from shapely.geometry import Polygon, MultiPolygon
import json
import os
import sys
import math


def create_sub_masks(mask_image):
    width, height = mask_image.size

    # Initialize a dictionary of sub-masks indexed by RGB colors
    sub_masks = {}
    for x in range(width):
        for y in range(height):
            # Get the value returned by getpixel() directly
            pixel_value = mask_image.getpixel((x, y))

            # Get the RGB values of the pixel
            pixel = pixel_value[:3]

            # If the pixel is not black and white (白は茎の部分)
            if pixel != (0, 0, 0) and pixel != (255, 255, 255):
                # Check to see if we've created a sub-mask...
                pixel_str = str(pixel)
                sub_mask = sub_masks.get(pixel_str)
                if sub_mask is None:
                   # Create a sub-mask (one bit per pixel) and add to the dictionary
                    # Note: we add 1 pixel of padding in each direction
                    # because the contours module doesn't handle cases
                    # where pixels bleed to the edge of the image
                    sub_masks[pixel_str] = Image.new('1', (width+2, height+2))

                # Set the pixel value to 1 (default is 0), accounting for padding
                sub_masks[pixel_str].putpixel((x+1, y+1), 1)

    return sub_masks


def create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd):
    # Find contours (boundary lines) around each sub-mask
    # Note: there could be multiple contours if the object
    # is partially occluded. (E.g. an elephant behind a tree)
    contours = measure.find_contours(np.array(sub_mask), 0.5, positive_orientation='low')

    segmentations = []
    polygons = []
    for contour in contours:
        # Flip from (row, col) representation to (x, y)
        # and subtract the padding pixel
        for i in range(len(contour)):
            row, col = contour[i]
            contour[i] = (col - 1, row - 1)

        # Make a polygon and simplify it
        poly = Polygon(contour)
        poly = poly.simplify(1.0, preserve_topology=False)
        polygons.append(poly)
        segmentation = np.array(poly.exterior.coords)
        segmentation = np.maximum(segmentation, 0).ravel().tolist()
        if len(segmentation) != 0: # 空リストを除外
            segmentations.append(segmentation)

    # セグメンテーションがない場合はスキップ
    if len(segmentations) == 0:
        return "skip"

    # Combine the polygons to calculate the bounding box and area
    multi_poly = MultiPolygon(polygons)
    if multi_poly.bounds == ():
        return "skip"
    x, y, max_x, max_y = multi_poly.bounds
    # x = max(0, x)
    # y = max(0, y)
    width = max_x - x
    height = max_y - y
    bbox = (x, y, width, height)
    area = multi_poly.area

    annotation = {
        'segmentation': segmentations,
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': bbox,
        'area': area
    }

    return annotation


def get_name(root, mode_folder=True):
    for root, dirs, file in os.walk(root):
        if mode_folder:
            return sorted(dirs)
        else:
            return sorted(file)


def get_annotation(rrr, output_name):
    mask_image_root = get_name(rrr, mode_folder=False)
    dataset = {"images": [],
               "annotations": [],
               "categories": []}
    class_index = {1: "grape_berry"}
    for s, k in enumerate(list(class_index.keys())):
        dataset["categories"].append({"id": k, "name": class_index[k]})

    is_crowd = 0

    # These ids will be automatically increased as we go
    annotation_id = 0
    image_id = 0

    # Create the annotations
    for i, root in enumerate(mask_image_root):
        print(i)
        mask_image = Image.open(rrr + root).convert("RGB")
        print(root)
        weight, height = mask_image.size
        dataset["images"].append({"license": 1,
                                  "file_name": root,
                                  "id": i,
                                  "width": weight,
                                  "height": height})
        sub_masks = create_sub_masks(mask_image)
        for _, sub_mask in sub_masks.items():
            category_id = 1
            annotation = create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd)
            if annotation == "skip":
                continue
            dataset["annotations"].append(annotation)
            annotation_id += 1
        image_id += 1
    with open("{}{}".format(rrr, output_name), "w") as f:
        json.dump(dataset, f)

args = sys.argv
# 処理対象のフォルダを取得
if len(args) == 1:
    print("フォルダのパスを第1引数で指定してください") # data/path_to_image_folder/
    exit()
rrr = args[1]

# 出力ファイル名を指定
output_name = "annotation_coco.json"
if len(args) > 2:
    output_name = args[2]

# フォルダ内の画像からアノテーションを作成
print("preprocessing start with {}".format(rrr))

get_annotation(rrr, output_name)
