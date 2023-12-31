import os
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image

import numpy as np


classes = ["丸顔","細顔"]
image_size = 50

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('pymodel.h5', compile=False)#学習済みモデルをロード


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換
            img = image.load_img(filepath, target_size=(image_size,image_size))
            img = image.img_to_array(img)
            data = np.array([img])
            
            
       #変換したデータをモデルに渡して予測する
        if request.method == 'POST':
        # ... (existing code)

           result = model.predict(data)[0]
           predicted = result.argmax()
           pred_answer = "これは " + classes[predicted] + " です"

        # Save the image to the appropriate folder
        if pred_answer == "丸顔":
            save_folder = "marugao"
        else:
            save_folder = "hosogao"

        os.makedirs(os.path.join(UPLOAD_FOLDER, save_folder), exist_ok=True)
        file.save(os.path.join(UPLOAD_FOLDER, save_folder, filename))

        image_list = os.listdir(os.path.join(UPLOAD_FOLDER, save_folder))
        print(image_list)


        return render_template("index.html", answer=pred_answer, image_folder=save_folder , image_list=image_list)

    return render_template("index.html", answer="")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)