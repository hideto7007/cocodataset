# cocodataset


## cocodataset作成ツール

### 事前準備
 - dataset/<project_name>のディレクトリ作成
 - 作成したディレクトリ内に以下のデータを格納
   - train, val⇒画像
   - train_annotations, val_annotations⇒画像のアノテーション


ディレクトリ階層  
```
datasets/  
   -coco/  
        -train/  # 訓練画像
            -000000000001.jpg  
            -000000000002.jpg  
            -000000000003.jpg  
        -val/    # 検証画像
            -000000000004.jpg  
            -000000000005.jpg  
            -000000000006.jpg   
        -test/   # 評価画像
            -000000000004.jpg  
            -000000000005.jpg  
            -000000000006.jpg   
        -annotations  
            -instances_train.json  
            -instances_val.json 
            -instances_test.json

```  

※test_dataがある場合別で作成する

### valが存在しない場合
 - train_val_split.shを実行してtrainの1割をvalにする
 - スクリプトの引数には、datatset/<project_name>とする


### cocodataset作成
 - coco.shの引数<project_name>を対象の名前に変更する
 - スクリプト実行


### テスト(評価データ)のcocodatasetを作成する場合
 - coco.shと同様に変更する



#### coco.sh
```
    #!/bin/bash

    echo 'coco.pyバッチ実行'
    echo 'annotationsディレクトリかつjsonファイル作成'
    project_name=library_data  # 自信のプロジェクト名に変更
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

```
