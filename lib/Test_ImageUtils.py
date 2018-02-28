import cv2
import numpy as np

def LoadImages(imagesList):
    matList = []
    for i in range(len(imagesList)):
        im = cv2.imread(imagesList[i])
        matList.append(im)
    return matList

def IsDarkCharLightBack(binMat):
    count = 0
    coordX = [0, 1, 0, 1,\
    binMat.shape[0]-1, binMat.shape[0]-2, binMat.shape[0]-1, binMat.shape[0]-2,\
    0, 1, 0, 1,\
    binMat.shape[0]-1, binMat.shape[0]-2, binMat.shape[0]-1, binMat.shape[0]-2]
    coordY = [0, 0, 1, 1,\
    0, 0, 1, 1,\
    binMat.shape[1]-1, binMat.shape[1]-1, binMat.shape[1]-2, binMat.shape[1]-2,\
    binMat.shape[1]-1, binMat.shape[1]-1, binMat.shape[1]-2, binMat.shape[1]-2]
    for ind in range(16):
        if binMat[coordX[ind]][coordY[ind]] < 125:
            count += 1
        else: count -= 1
    return (True if count < 0 else False)

def BinImage(grayImage):
    threshold,binImage = cv2.threshold(grayImage,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    return binImage

def GrayImage(img):
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    return img

def IsGrayImage(img):
    if img.shape[2] == 1:
        return True
    else:
        return False# or True

def GetMeanStd(grayImage, binImage, preOrBack):
    valuelist = []
    #grayImage = cv2.blur(grayImage, cv2.Size(5, 5))
    rows = grayImage.shape[0]
    cols = grayImage.shape[1]
    if IsDarkCharLightBack(binImage):
        if preOrBack == 'back':
            for i in range(rows):
                for j in range(cols):
                    if binImage[i,j] == 255:
                        valuelist.append(grayImage[i,j])
        else:
            for i in range(rows):
                for j in range(cols):
                    if binImage[i,j] == 0:
                        valuelist.append(grayImage[i, j])
    else:
        if preOrBack == 'back':
            for i in range(rows):
                for j in range(cols):
                    if binImage[i,j] == 0:
                        valuelist.append(grayImage[i, j])
        else:
            for i in range(rows):
                for j in range(cols):
                    if binImage[i,j] == 255:
                        valuelist.append(grayImage[i, j])
    if len(valuelist) < 5:
        mean = -1.0
        stddev = -1.0
        return mean, stddev
    targetArray = np.array(valuelist)
    mean = targetArray.mean()
    stddev = targetArray.std()
    stddev = max(stddev, 2.0)

    return mean, stddev
