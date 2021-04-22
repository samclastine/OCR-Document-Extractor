
from extractor.pan import *
from extractor.aadhar import *
from extractor.licence import *
import cv2
from os import path


def text_detection(image_file, doc_type):
  
    img = cv2.imread(image_file)

    if doc_type == "Pancard":

        # get details from the image
        pan_details = get_pan_number(image_file)
        return pan_details
    elif doc_type == "Aadhar_Card":

        aadhar_details = get_aadhar_text(image_file)
        return aadhar_details
    elif doc_type == "Driving_Licence":

        # recognize raw text first

        license_details = get_licence_texts(image_file)
        return license_details

    else:
        return "No text found"


