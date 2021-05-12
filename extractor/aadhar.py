import cv2
import numpy as np
import json
import os.path
import os
import re
import numpy as np
import pytesseract
import io
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def cleanup_text(text):
    text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
    # create a list of unwanted word to remove in lower case only
    remove = ["permanent", "account", "income","tax", "number", "card", "department", "name", "father'", "father's", "father", "of", "signature",
              "govt.", "india", "card", "birth", "date", "fathers", "ante", "twat", "TOA QAHT), THA HML Wend","Number.","_ UMHS ret /"," ahe0ot /"]
    print(text)


def get_aadhar_text(image_file):
    imp={}
    aad_details={}
    img = cv2.imread(image_file)

    # resize the image
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # convert the image to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh1=cv2.threshold(src=img,thresh=150,maxval=255,type=cv2.THRESH_BINARY)
    
    texts = pytesseract.image_to_string(img)

    if re.search(r"[0-9]{4}\s[0-9]{4}\s[0-9]{4}", texts):
                try:
                    imp['Aadhar No'] = re.findall(r"[0-9]{4}\s[0-9]{4}\s[0-9]{4}", texts)[0]
                except Exception as _:
                    imp['Aadhar No'] = "Not Found"


    if 'Female' in texts or 'FEMALE' in texts:
        imp['gender'] = "Female"
    if 'Male' in texts or 'MALE' in texts:
        imp['gender'] = "Male"


    if re.search(r"[A-Z]{3} : [0-9]{2}\-|/[0-9]{2}\-|/[0-9]{4}", texts):
                
                try:
                    imp["Date of Birth"] = re.findall(r"[0-9]{2}\-[0-9]{2}\-[0-9]{4}", texts)[0]
                except Exception as _:
                    imp["Date of Birth"] = re.findall(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", texts)[0]

    
    if len(texts.split(' ')) > 2:
                
                if 'GOVERNMENT' in texts or 'OF' in texts or 'INDIA' in texts:
                    pass
                else:
                    imp["Name"] = re.findall(r"[A-Za-z]{3} [A-Za-z]{8}", texts)[0]
    return imp



#if __name__=="__main__":
    #imagepath=r"C:\Users\Clastine\Downloads\DOC 1 19A515_1.jpg"
    #imgp = cv2.imread(imagepath)
    #get_aadhar_text(imagepath)
    