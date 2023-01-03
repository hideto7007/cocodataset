#!/bin/bash


echo 'train_val_split.pyバッチ実行'
data_path="./dataset/library_data"
python train_val_split.py $data_path 
echo 'train_val_split.pyバッチ終了'
echo $?