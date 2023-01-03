## cocodataset作成ツール

### 事前準備
 - train, val⇒画像
 - train_annotations, val_annotations⇒画像のアノテーション

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