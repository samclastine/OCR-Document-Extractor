from PIL import Image
import pytesseract
import datetime
import sys
import os
import os.path
import re
import cv2
import numpy as np
import datefinder
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

list_of_states={'JK','HP','PN','CH','UK','UA','HR','DL','RJ','UP','BR','SK','AR','AS','NL','MN','ML','TR','MZ','WB','JH','OR','OD','CG','MP','GJ','MH','DD','DN','TS','AP','KA','KL','TN','PY','GA','AN','LD'}
strings_with_states=[]


def get_licence_texts(image_file):
    imp={}
    count=0
    img = cv2.imread(image_file)

    # resize the image
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # convert the image to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh1=cv2.threshold(src=img,thresh=150,maxval=255,type=cv2.THRESH_BINARY)
    # the following command uses the tesseract directory path to get the trained data in the config option
    texts = pytesseract.image_to_string(thresh1)
    res=texts.split()

    expdates=list(datefinder.find_dates(texts))[-1]
    imp ['Date of expiry']=expdates.strftime('%d/%m/%Y')

    if re.search(r"[A-Z]{3} : [0-9]{2}\-|/[0-9]{2}\-|/[0-9]{4}", texts):
                # if string similar to date is found, use it as a hook to find other details
                try:
                    imp["Date of Birth"] = re.findall(r"[0-9]{2}\-[0-9]{2}\-[0-9]{4}", texts)[0]
                except Exception as _:
                    imp["Date of Birth"] = re.findall(r"[0-9]{2}/[0-9]{2}/[0-9]{4}", texts)[0]



    for word in res:
        for state in list_of_states:
            if state in word:
                strings_with_states.append(word)
#get the driving licence # from the strings with state codes
    for string in strings_with_states:
        for i in string:
            if(i.isdigit()):
                count=count+1
        
        if count<13:
            index=res.index(string)
            s=res[index] + res[index +1]
            if len(s)>=15:
                for i in s:
                    if(i.isdigit()):
                        count=count+1
                if count>13:
                    s=s[-16:]
                    imp['Driving licence ']=s
                    break
                    break
        else:
            imp['Driving licence ']=string
            break
            break
    if 'Name' in res:
        index=res.index('Name')
        imp['Name of licence holder'] = (res[index+1]+ ' ' + res[index+2]+' ' + res[index+3])
    return imp

    


