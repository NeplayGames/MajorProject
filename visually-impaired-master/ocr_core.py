import pytesseract
import cv2


def mark_region():
    pytesseract.pytesseract.tesseract_cmd = 'E:\\OCr\\tesseract.exe'
    im = cv2.imread("accept.jpg")
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blurs = cv2.GaussianBlur(gray, (9, 9), 0)
    text = str(pytesseract.image_to_string(im, config='--psm 6'))
    return text
