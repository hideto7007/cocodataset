#!/bin/bash


echo 'coco_test.pyバッチ実行'
project_name=library_data
cd ./dataset/$project_name/annotations/
touch instances_test.json
cd -

echo 'instances_test.json作成'
img_path="./dataset/$project_name/test/"
json_path="./dataset/$project_name/test_annotations/"
write_json="./dataset/$project_name/annotations/instances_test.json"
python coco.py $img_path $json_path $write_json
echo 'instances_test.json作成終了'
'
echo $?