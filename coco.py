"""
    train, valアノテーション作成ツール
"""

import os
import cv2
import json
import glob
import sys
import collections


# EfficientDetの場合、'iscrowd': 0をannotationファイル(dict)に追加する
# 0は人間以外の領域を判別、1は人間の領域を判別

# 画像が格納されたディレクトリ名
image_dir = sys.argv[1]
annot_dir = sys.argv[2]
write_json = sys.argv[3]

# カテゴリ名をカテゴリIDにマッピングする辞書の定義
category_map = {
    '1_overall': 1,
    '2_handwritten': 2,
    '3_typography': 3,
    '4_illustration': 4,
    '5_stamp': 5, 
    '6_headline': 6,
    '7_caption': 7,
    '8_textline': 8,
    '9_table': 9,
}

# categoriesリストの作成
categories = [
    {'id':1, 'name': '1_overall'},
    {'id':2, 'name': '2_handwritten'},
    {'id':3, 'name': '3_typography'},
    {'id':4, 'name': '4_illustration'},
    {'id':5, 'name': '5_stamp'},
    {'id':6, 'name': '6_headline'},
    {'id':7, 'name': '7_caption'},
    {'id':8, 'name': '8_textline'},
    {'id':9, 'name': '9_table'}
]

def make_image_data(image_dir):
    """imagesデータ作成"""

    # 全ての画像のファイル名をリストとして取得する
    imfile_name_list = os.listdir(image_dir)

    # 画像IDの初期化
    image_id = 1

    # リストの初期化
    images = []

    # 各画像ごとの情報をひとつずつ取得
    for imfile_name in imfile_name_list:
    
        # 画像のファイルパスを指定
        image_path = image_dir + imfile_name
        
        # 画像の読み込み
        image = cv2.imread(image_path)
        
        # 画像の高さ、幅を取得
        im_height, im_width, _ = image.shape

        # 画像1枚分の情報を辞書にまとめる
        image_dict = {
            'file_name': imfile_name,
            'height': im_height,
            'width': im_width,
            'id': image_id
        } 
        
        # 完成した画像1枚分の情報をimagesリストへ追加
        images.append(image_dict)
        
        # 画像IDを+1して次の画像へ
        image_id += 1
        
    return images


def make_annotations_data(image_dir, category_map, annot_dir):
    """annotationsデータ作成"""

    imfile_name_list = os.listdir(image_dir)
    image_id = 1
    images = []

    # 物体IDの初期化
    annot_id = 1

    # annotationsリストの初期化
    annotations = []

    for imfile_name in imfile_name_list:
    
        image_path = image_dir + imfile_name
        image = cv2.imread(image_path)
        im_height, im_width, _ = image.shape
        image_dict = {
            'file_name': imfile_name,
            'height': im_height,
            'width': im_width,
            'id': image_id
        } 
        images.append(image_dict)
        
        ### ここからannotationsリストに含める情報の取得へ ###
        # 画像と対応するアノテーションファイルのパスの指定
        annot_path = annot_dir + imfile_name.replace('jpg', 'json')
        
        # JSONファイルの読み込み
        with open(annot_path, encoding='utf-8') as f:
            annot = json.load(f)
        # 対象画像内の全物体に対するアノテーション情報リストの取得
        labels = annot['labels']
        
        # 各物体ごとのアノテーション情報をひとつずつ取得
        for label in labels:
            
            # バウンディングボックス位置情報の取得
            x1 = label['box2d']['x1']
            y1 = label['box2d']['y1']
            x2 = label['box2d']['x2']
            y2 = label['box2d']['y2']
            
            # bboxの高さ、幅の取得
            # (bboxの位置情報の表し方をXYXY形式 -> XYWH形式 に変更するため)
            box_width = x2 - x1
            box_height = y2 - y1
            
            # カテゴリIDの取得
            category = label['category']
            category_id = category_map[category]
                    
            # 物体1つ分の情報を辞書にまとめる
            annot_dict = {
                'image_id': image_id,
                'bbox': [x1, y1, box_width, box_height],
                'category_id': category_id,
                'id': annot_id,
                'iscrowd': 0
            }
            
            # 完成した物体1つ分の辞書型データをannotationsリストへ追加
            annotations.append(annot_dict)
            
            # 物体IDを+1して次の物体へ
            annot_id += 1
            
        image_id += 1
    
    return annotations


def make_image_json_combi(category_map, categories, image_dir, annot_dir, images, annotations, write_json):
    """JSON(imageとannotationsデータ組み合わせ)ファイルを生成する"""


    # 全ての画像のファイル名をリストとして取得
    imfile_name_list = os.listdir(image_dir)

    # 画像ID, 物体IDの初期化
    image_id = 1
    annot_id = 1

    # リストの初期化
    images = []
    annotations = []

    # 各画像ごとの情報をひとつずつ取得
    for imfile_name in imfile_name_list:
    
        # 画像のファイルパスの指定
        image_path = image_dir + imfile_name
        # この画像と対応するアノテーションファイルのパスの指定
        annot_path = annot_dir + imfile_name.replace('jpg', 'json')
        
        # 画像の読み込み
        image = cv2.imread(image_path)
        
        # 画像の高さ、幅を取得
        im_height, im_width, _ = image.shape

        # 画像1枚分の情報を辞書にまとめる
        image_dict = {
            'file_name': imfile_name,
            'height': im_height,
            'width': im_width,
            'id': image_id
        } 
        
        # 完成した画像1枚分の情報をimagesリストへ追加
        images.append(image_dict)
        
        # JSONファイルを読み込み、
        # この画像内の全物体に対するアノテーション情報リスト取得
        with open(annot_path, encoding='utf-8') as f:
            annot = json.load(f)
        labels = annot['labels']
        
        # 各物体ごとのアノテーション情報をひとつずつ取得
        for label in labels:
            # bboxの位置情報の取得
            x1 = label['box2d']['x1']
            y1 = label['box2d']['y1']
            x2 = label['box2d']['x2']
            y2 = label['box2d']['y2']
            
            # bboxの高さ、幅の取得
            # (バウンディングボックスの位置情報の表し方をXYXY形式 -> XYWH形式 に変更するため)
            box_width = x2 - x1
            box_height = y2 - y1
            
            # カテゴリIDの取得
            category = label['category']
            category_id = category_map[category]
                    
            # 物体1つ分のアノテーション情報を辞書にまとめる
            annot_dict = {
                'image_id': image_id,
                'bbox': [x1, y1, box_width, box_height],
                'category_id': category_id,
                'id': annot_id,
                'iscrowd': 0
            }
            
            # 完成した物体1つ分の情報をannotationsリストへ追加
            annotations.append(annot_dict)
            
            # 物体IDを+1して次の物体へ
            annot_id += 1
            
        # 画像IDを+1して次の画像へ
        image_id += 1

    # COCO フォーマットと同様の構造を持つ辞書型データの作成
    print("cocoフォーマット作成")
    coco_format_dict = {
        'images': images,
        'annotations': annotations,
        'categories': categories,
        'iscrowd': 0
    }

    # 作成したCOCO フォーマットのアノテーションをJSONファイルに保存
    with open(write_json, 'w') as f:
        json.dump(coco_format_dict, f)

    # 作成したCOCO フォーマットのアノテーションデータを表示
    print('--------------')
    print('images')
    print('--------------')
    print(coco_format_dict['images'])

    print('--------------')
    print('annotations')
    print('--------------')
    print(coco_format_dict['annotations'])

    print('--------------')
    print('categories')
    print('--------------')
    print(coco_format_dict['categories'])


    
make_images = make_image_data(image_dir)
make_annotations = make_annotations_data(image_dir, category_map, annot_dir)
make_image_json_combi(category_map, categories, image_dir, annot_dir, make_images, make_annotations, write_json)