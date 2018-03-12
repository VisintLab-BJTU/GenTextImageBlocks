#/usr/bin/python
#-*-coding=UTF-8-*-
# --------------------------------------------------------
# GenTextBlocks
# Copyright (c) 2017 VisInt
# Licensed under The MIT License [see LICENSE for details]
# Written by Jing Zhang and Wenyuan Xue
# --------------------------------------------------------
import cv2
import numpy as np

#输入：含有图像完整路劲的list
#输出：根据路劲载入图像，并返回一个mat类型的list
def LoadImages(imagesList):
    matList = []
    for i in range(len(imagesList)):
        im = cv2.imread(imagesList[i])
        matList.append(im)
    return matList

#输入：二值图像
#输出：判断图像是否为黑字白底，参考src/ImageUtils.cpp中的实现，输出True或者False
def IsDarkCharLightBack(binMat):
    count = 0
    rows = binMat.shape[0]
    cols = binMat.shape[1]
    dx = [0,1,0,1,rows-1,rows-2,rows-1,rows-2,0,1,0,1,rows-1,rows-2,rows-1,rows-2]
    dy = [0,0,1,1,0,0,1,1,cols-1,cols-1,cols-2,cols-2,cols-1,cols-1,cols-2,cols-2]
    for i in range(16):
        if binMat[dx[i],dy[i]]<125:
            count+=1
        else:
            count-=1
    return (True if count < 0 else False)

#输入：灰度图
#输出：二值图(用OTSU的方法)
def BinImage(grayImage):
    threshold,binImage = cv2.threshold(grayImage,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    return binImage

#输入：一张图像
#输出：判断是否为灰度图，输出True或者False
def IsGrayImage(img):
    if len(img.shape)==2:
        return True
    else:
        return False# or True

#输入：rgb三通道图像
#输出：灰度图
def GrayImage(img):
    if IsGrayImage(img):
        return img
    else:
        img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        return img

#输入：灰度图，二值图，目标背景(前景或后景)
#输出：前景(或后景)的均值，标准差(浮点型),参考./src/TemplateImaeg.cpp中的实现
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
        return mean,stddev
    targetArray = np.array(valuelist)
    mean = targetArray.mean()
    stddev = targetArray.std()
    stddev = max(stddev,2.0)

    return mean, stddev
