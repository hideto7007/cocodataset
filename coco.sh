#!/bin/bash

echo 'coco.pyバッチ実行'
echo 'annotationsディレクトリかつjsonファイル作成'
project_name=library_data
mkdir ./dataset/$project_name/annotations
cd ./dataset/$project_name/annotations/
touch instances_train.json
touch instances_val.json
cd -
echo 'annotationsディレクトリかつjsonファイル作成終了'

echo 'instances_train.json作成'
img_path="./dataset/$project_name/train/"
json_path="./dataset/$project_name/train_annotations/"
write_json="./dataset/$project_name/annotations/instances_train.json"
python coco.py $img_path $json_path $write_json
echo 'instances_train.json作成終了'

echo 'instances_val.json作成'
img_path="./dataset/$project_name/val/"
json_path="./dataset/$project_name/val_annotations/"
write_json="./dataset/$project_name/annotations/instances_val.json"
python coco.py $img_path $json_path $write_json
echo 'instances_val.json作成終了'
echo $?