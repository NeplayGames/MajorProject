import cv2 as cv
import numpy as np
from ocr_core import mark_region

###################################
widthImg = 540
heightImg = 640


#####################################

def Main():
    img = cv.imread("accept.jpg")

    img = cv.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThrees = preProcessing(img)
    biggest = getContours(imgThrees, imgContour)
    print(biggest)
    if biggest.size != 0:
        print("I AM Here")
        imgWarped = getWarp(img, biggest)
        cv.imwrite("accept.jpg", imgWarped)
    return mark_region()


def preProcessing(img):
    img = cv.medianBlur(img, 5)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(img, (5, 5), 0)
    _, blackAndWhiteImage = cv.threshold(blur, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cv.imwrite("2.jpg", blackAndWhiteImage)
    return blackAndWhiteImage


def getContours(img, imgContour):
    biggest = np.array([])
    maxArea = 0
    contours, _ = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        print(area)
        # cv.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
        peri = cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
        if area > maxArea and len(approx) == 4:
            biggest = approx
            maxArea = area
    print("This is max area " + str(maxArea))
    cv.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    # print("add", add)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return myPointsNew


def getWarp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCropped = cv.resize(imgCropped, (widthImg, heightImg))
    # imgCropped = cv2.circle(imgCropped,(400,50),30,(0,0,255),cv2.FILLED)
    return imgCropped
