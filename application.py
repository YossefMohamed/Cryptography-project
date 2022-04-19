from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from skimage import color
from skimage import io
from PIL import Image



app = Flask(__name__)


app.secret_key = "secret key"
app.config['SESSION_TYPE'] = 'filesystem'
app.config["UPLOAD_FOLDER"] = "static/uploads"

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.htm")

@app.route('/encryption',methods=['POST'])
def encryption():
    if 'file' not in request.files:
        flash("No Images Found")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("No image selected for uploading")
        return render_template("index.htm")
    if file and allowed_file(file.filename):
        filename = file.filename
        imgPath = os.path.join(app.config['UPLOAD_FOLDER'], filename) # get the path of the image
        file.save(imgPath)
        img = Image.open(imgPath)
        imgGray = img.convert('L')
        imgGray.save(imgPath)
        return render_template("index.htm",filename=filename)
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return render_template("index.htm")



@app.route('/decryption',methods=['POST'])
def decryption():    
    if 'file' not in request.files:
        flash("No Images Found")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("No image selected for uploading")
        return render_template("index.htm")
    if file and allowed_file(file.filename):
        filename = file.filename
        imgPath = os.path.join(app.config['UPLOAD_FOLDER'], filename) # get the path of the image
        file.save(imgPath)
        print(filo)
        img = Image.open(imgPath)
        imgGray = img.convert('L')
        imgGray.save(imgPath)
        return render_template("index.htm",filename=filename)
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return render_template("index.htm")


if __name__ == "__main__":
    app.run(debug=True)