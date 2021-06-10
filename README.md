# Resistor Checker
抵抗器の抵抗値を画像から判別するアプリケーション

## Version
* python-3.7.10

## 実行コマンド
1. ライブラリのインストール

```
pip install -r requirements.txt
```

2. webサーバーの起動（local）

```
python app.py
```


上記を実行後、以下のエラー

```
module 'tensorflow.python.keras.utils.generic_utils' has no attribute 'populate_dict_with_module_objects'
```

が出た場合、以下のコマンドを実行することで解決。
（https://github.com/tensorflow/tensorflow/issues/38012）

```
pip list | grep tf
pip install tensorflow --upgrade --force-reinstall
```


## reference
* [HerokuにFlaskアプリをデプロイ](https://qiita.com/redpanda/items/a056daea48b545250ce7)