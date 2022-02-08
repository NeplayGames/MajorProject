import cv2
import numpy as np
from ocr_core import mark_region

###################################
widthImg = 540
heightImg = 640


#####################################

def Main():
    img = cv2.imread("accept.jpg")

    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThrees = preProcessing(img)
    biggest = getContours(imgThrees, imgContour)
    print(biggest)
    if biggest.size != 0:
        print("I AM Here")
        imgWarped = getWarp(img, biggest)
        cv2.imwrite("accept.jpg", imgWarped)
    return mark_region()


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    (thresh, blackAndWhiteImage) = cv2.threshold(imgBlur, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite("2.jpg", blackAndWhiteImage)
    return blackAndWhiteImage


def getContours(img, imgContour):
    biggest = np.array([])
    maxArea = 0
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if area > maxArea and len(approx) == 4:
            biggest = approx
            maxArea = area
    print("This is max area " + str(maxArea))
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
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
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))
    # imgCropped = cv2.circle(imgCropped,(400,50),30,(0,0,255),cv2.FILLED)
    return imgCropped
