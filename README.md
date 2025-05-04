## Origin repo
https://github.com/open-mmlab/mmdetection

## Directory structure
Basically this repo is same as the origin repo

Added
- grape/ : main folder 
  - raw_data/ : data for learning and estimation
  - data/ : processed data
  - preprocess/ : preprocess utils
  - mmdetection.ipynb : learning and estimation

- fisheye_to_cubemap/ : Utils for fisheye image

## Getting Started
### 1. Make conatiner from docker/docker-compose
```
cd docker
docker-compose up -d
```

参考：　https://bo-li.medium.com/how-to-use-mmsegmentation-docker-image-and-mount-local-drive-3c16fa048d15

### 2. install dependencies(if you need)
```
cd mmdetection
pip install -r requirements.txt
```

### 3. make annotation for data set
```
cd grape/preprocess
sh annotation.sh [input_dir]
```

ex)：sh annotation.sh /mmdetection-grape/grape/data/resize_blur5

### 4. annotationファイルを修正
color画像はJPG、label画像はpngであるため、annotationファイルを修正する

annotationファイルを開いてpngをJPGに変換

### 5.Train model and estimate in grape/mmdetection.ipyn
```
jupyter lab --port 8888 --no-browser --ip=0.0.0.0 --allow-root
```

