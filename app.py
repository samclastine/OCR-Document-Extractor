from flask import Flask
from flask import render_template,request
import os
from processings import text_detection
from werkzeug.utils import secure_filename
import cv2


app=Flask(__name__,template_folder='template')

UPLOAD_FOLDER='uploads'
@app.route("/",methods=["GET","POST"])
def upload_predict():
    details = {"extract" : ""}
    if request.method == "POST":
        image_file = request.files["image"]
        doc_type = request.form["type"]
        if not os.path.exists(UPLOAD_FOLDER + doc_type):
            os.mkdir(UPLOAD_FOLDER + doc_type)

        img_name = secure_filename(image_file.filename)
        

        save_path = UPLOAD_FOLDER + doc_type + "/" + img_name
        image_file.save(save_path)
        
        details = text_detection(save_path, doc_type)
    return render_template("index.html",extract=details)




if __name__ == "__main__":
    
    app.run(port=5000,debug=True)