# annotations

import os
import json
import glob
import sys
import math
import shutil


data_path = sys.argv[1]

for i in ["val", "val_annotations"]:
    os.makedirs(data_path+"/"+i, exist_ok=True)

def has_duplicates(seq):
    return len(seq) != len(set(seq))


def file_move(path):
    """train_valで分ける"""
    
    dir_list = [i for i in os.listdir(path)]
    
    file_list = [ os.listdir(path + "/" + dirs) for dirs in dir_list ]
    file_count = [ len(os.listdir(path + "/" + dirs)) for dirs in dir_list ]
    
    val_num = math.ceil(file_count[0] * 0.1)
    
    
    for imgs, jsons in zip(file_list[0][:val_num], file_list[1][:val_num]):
        val_img = imgs.replace(dir_list[0], dir_list[2])
        val_json = jsons.replace(dir_list[0], dir_list[2])
        shutil.move(path+"/"+dir_list[0]+"/"+imgs, path+"/"+dir_list[2]+"/"+val_img)
        shutil.move(path+"/"+dir_list[1]+"/"+jsons, path+"/"+dir_list[3]+"/"+val_json)


file_move(data_path)
            

