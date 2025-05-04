# 学習データのアノテーションを行うスクリプト
input_dir=$1
python Mask2polygon.py $input_dir/train/label/
python Mask2polygon.py $input_dir/val/label/