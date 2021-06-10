# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import numpy as np
import os, io
from PIL import Image
from PIL import ImageFile
import base64
from cnn_model import def_model, get_model

app = Flask(__name__)

@app.route('/',methods = ['GET', 'POST'])
def index():
    return render_template('input.html')

@app.route('/send', methods = ['POST'])
def posttest():
    if request.files['img_file']:
        img_file = request.files['img_file']
        fileName = img_file.filename
        photo_size=60

        #拡張子取り出し
        root, ext = os.path.splitext(fileName)
        ext = ext.lower()

        #拡張子判別
        gazouketori = set([".jpg", ".jpeg", ".jpe", ".jp2", ".png", ".webp", ".bmp", ".pbm", ".pgm", ".ppm",
                              ".pxm", ".pnm",  ".sr",  ".ras", ".tiff", ".tif", ".exr", ".hdr", ".pic", ".dib"])

        if ext not in gazouketori:
            return render_template('input.html',massege = "対応してない拡張子です",color = "red")

        labels = ["10","22","47",
                  "100","220","470",
                  "1k","2.2k","4.7k",
                  "10k","22k","47k",
                  "100k","220k","470k",
                  "1M","2.2M"]

        model= get_model((photo_size,photo_size,3),17)#画像のshape、ラベルデータの数
        model.load_weights("./photo_size=60_batch_size=32_epochs=23_per=97.5_.hdf5")

        img=Image.open(img_file)
        img=img.resize((photo_size,photo_size))#画像のshape
        img=img.convert("RGB")

        #arrayに変換
        x=np.asarray(img)
        x=x.reshape(-1,photo_size,photo_size,3)#画像のshape
        x=x/255

        #予測
        pre=model.predict([x])[0]
        idx=pre.argmax()
        per=str(int(pre[idx]*100))
        answer=labels[idx]

        #画像書き込み用バッファに画像を保存してhtmlに返す
        #(画像ファイルを静的に保存しないで、render_template()を使って表示する方法　)
        #https://teratail.com/questions/89341
        buf = io.BytesIO()
        image = Image.open(img_file)
        image.save(buf, 'png')
        qr_b64str = base64.b64encode(buf.getvalue()).decode("utf-8")
        qr_b64data = "data:image/png;base64,{}".format(qr_b64str)
        return render_template('output.html',answer = answer ,img = qr_b64data, percentage=per)

#pythonインタープリタからの実行時のみサーバで起動し、モジュールとしてインポートされたときには起動しない
if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
