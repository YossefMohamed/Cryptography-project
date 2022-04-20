from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from skimage import color
from skimage import io
from PIL import Image
from Crypto.Cipher import DES3
from hashlib import md5
from helper import Encryption
from helper import Decryption
import cv2
import math
import numpy as np
from flask import send_from_directory


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
        img = cv2.imread(imgPath, 1)   
        
        EncryptionImg = np.zeros(img.shape, np.uint8)
        Encryption(img,10,30,0.123345,EncryptionImg)                                       # encryption
        cv2.imwrite(f"./static/uploads/encrypted{filename}",EncryptionImg)  # Save the encrypted image
        #send_from_directory("./static/uploads/", filename=f'encrypted{filename}')
        print('Operation Done!')
        return render_template("index.htm",filename=f'encrypted{filename}')
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
        # img = Image.open(imgPath)
        # imgGray = img.convert('L')
        # imgGray.save(imgPath)

        img = cv2.imread(imgPath, 1)        # Read decrypted image
        print(img)
        DecryptionImg = np.zeros(img.shape, np.uint8)
        Decryption(img, 10, 30, 0.123345, DecryptionImg)                                   # decrypt
        cv2.imwrite(f"./static/uploads/decrypted{filename}", DecryptionImg) # Save the decrypted image
        
        return render_template("index.htm",filename=f'decrypted{filename}')
       
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return render_template("index.htm")



if __name__ == "__main__":
    app.run(debug=True)