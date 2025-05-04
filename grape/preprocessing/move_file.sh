# 「label/」と「color/」にファイルを移動するスクリプト

# 学習時に以下のディレクトリ構造が必要
# 任意のディレクトリ/
# ├── train/
# │   ├── color/
# │   ├── label/
# │   └── annotation_coco.json
# └── val/
#     ├── color/
#     ├── label/
#     └── annotation_coco.json

# 入出力先のディレクトリは適宜変更


# label.pngで終わるファイルをlabelディレクトリに移動
find /mmdetection/grape/data/fastgrape/grape/fuji/ -type f -name "*label.png" -exec mv {} /mmdetection/grape/data/fastgrape/grape/fuji/train/label/ \;

# ファイル名末尾のlabelを削除
find /mmdetection/grape/data/fastgrape/grape/fuji/train/label/ -type f -name "*label.png" -exec bash -c 'mv "$1" "${1/_label.png/.png}"' _ {} \;

# rgb.JPGで終わるファイルをcolorディレクトリに移動
find /mmdetection/grape/data/fastgrape/grape/fuji/ -type f -name "*rgb.JPG" -exec mv {} /mmdetection/grape/data/fastgrape/grape/fuji/train/color/ \;

# ファイル名末尾のrgbを削除
find /mmdetection/grape/data/fastgrape/grape/fuji/train/color/ -type f -name "*rgb.JPG" -exec bash -c 'mv "$1" "${1/_rgb.JPG/.JPG}"' _ {} \;