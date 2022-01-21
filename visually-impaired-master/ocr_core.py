try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import csv
import os
from pytesseract import Output

UPLOAD_FOLDER = 'static/uploads/'


def ocr_core(image):



    pytesseract.pytesseract.tesseract_cmd = 'E:\\OCr\\tesseract.exe'
    custom_config = r'--oem 3 --psm 6'
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (3, 3), 0)
    #thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # Morph open to remove noise and invert image
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
   # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    #invert = 255 - opening
    data = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
    print(data)
    return data

