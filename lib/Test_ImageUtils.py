#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import logging

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
        if binMat[coordX[ind],coordY[ind]] < 125:
            count += 1
        else: count -= 1
    return (True if count < 0 else False)

def BinImage(img):
    if IsGrayImage(img):
        threshold,binImage = cv2.threshold(img,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    else:
        grayImage = GrayImage(img)
        threshold,binImage = cv2.threshold(grayImage,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    return binImage

def IsGrayImage(img):
    if img.shape[2] == 1:
        return True
    else:
        return False# or True

def GrayImage(img):
    if IsGrayImage(img):
        return img
    else:
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        return img

def TextRegion(Image):
    binImg = BinImage(Image)
    if not IsDarkCharLightBack(binImg):
        tempM = np.ones(binImg.shape,dtype="uint8")*255
        binImg = cv2.subtract(tempM, binImg)
    xT = []
    yT = []
    for i in range(binImg.shape[0]):
        for j in range(binImg.shape[1]):
            #print(binImg[i,j])
            if binImg[i,j] == 0:
                xT.append(j)
                yT.append(i)
            elif binImg[i,j] != 255:
                logging.warning("ImageUtils.TextRegion. Image should be a binary mat.")
    xMin = min(xT)
    xMax = max(xT)
    yMin = min(yT)
    yMax = max(yT)
    return binImg[yMin:yMax,xMin:xMax]

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
